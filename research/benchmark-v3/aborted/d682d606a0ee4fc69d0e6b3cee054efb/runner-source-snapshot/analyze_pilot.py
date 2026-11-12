"""Offline calibration analysis; never imports a model transport or sends requests."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sqlite3

WEIGHTS={'easy':4,'medium':8,'hard':8}


def analyze(folder,ledger_path,report_path):
    folder=Path(folder)
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    source=json.loads((folder/'source-manifest.json').read_text(encoding='utf-8'))
    with (folder/'raw_results.csv').open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    db=sqlite3.connect(ledger_path)
    db.row_factory=sqlite3.Row
    calls=list(db.execute('SELECT * FROM requests WHERE experiment=? ORDER BY created',(manifest['experiment_id'],)))
    assert len(rows)==18 and all(r['state']=='complete' for r in calls)
    assert all(int(r['input_tokens'])+int(r['output_tokens'])==int(r['total_tokens']) for r in rows)
    assert sum(int(r['total_tokens']) for r in rows)==sum(r['total_tokens'] for r in calls)
    assert sum(int(r['llm_calls']) for r in rows)==len(calls)
    assert all(r['input_tokens']+(json.loads(r['response'])['usage'].get('precached_prompt_tokens') or 0)<=r['input_reserve'] and r['output_tokens']<=r['output_reserve'] for r in calls)
    for name,h in manifest['runner_sha256'].items():
        assert hashlib.sha256((folder/'runner-source-snapshot'/name).read_bytes()).hexdigest()==h,name
    for row in rows:
        task_calls=[c for c in calls if c['evaluation']==f"{manifest['experiment_id']}:{row['model']}:{row['architecture']}:{row['task_id']}:1"]
        row['cached_input_tokens']=sum(json.loads(c['response'])['usage'].get('precached_prompt_tokens') or 0 for c in task_calls)
        row['combined_budget_tokens']=int(row['total_tokens'])+row['cached_input_tokens']
        row['input_including_cache']=int(row['input_tokens'])+row['cached_input_tokens']
        row['provider_latency_seconds']=sum(c['latency'] for c in task_calls)
    with (folder/'calibration-analysis.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    total=sum(r['combined_budget_tokens'] for r in rows)
    provider_total=sum(int(r['total_tokens']) for r in rows)
    projected=sum(r['combined_budget_tokens']*WEIGHTS[r['difficulty']] for r in rows)
    billed_projected=sum(int(r['total_tokens'])*WEIGHTS[r['difficulty']] for r in rows)
    forecasts=[{'repeats':n,'main_tokens':projected*n,'main_provider_total':billed_projected*n,
                'pilot_plus_50pct_margin_plus_reservation':total+math.ceil(1.5*projected*n)+69632} for n in (1,2,3)]
    recommendation=max([f['repeats'] for f in forecasts if f['pilot_plus_50pct_margin_plus_reservation']<=850000] or [0])
    stats={'experiment_id':manifest['experiment_id'],'provider_total_tokens':provider_total,
           'combined_including_cache':total,'remaining_hard_budget':1000000-total,
           'remaining_target_budget':850000-total,'forecasts':forecasts,'recommended_repeats':recommendation}
    (folder/'calibration-budget.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
    lines=['# Benchmark v3: калибровочный пилот','',
           f"Пилот `{manifest['experiment_id']}` завершён: 18 из 18 запланированных оценок, {len(calls)} LLM-вызова. Основной эксперимент не запускался.",'',
           '## Реализация и проверка','',
           f"Использована замороженная реализация v2 из `{source['v2_path']}` на коммите `{source['git_revision']}` с прежними незакоммиченными изменениями. Все 19 Python-файлов совпали со снимком Lite; все замороженные файлы подготовки v3 совпали с preparation-manifest.json. Новый adapter явно проверяет путь и хеши. Старый main-branch benchmark не подставлялся. Все шесть архитектур сохранены; выбраны только три. Спецификации, ожидаемые ответы и исходные результаты v2 не менялись.",'',
           'Протокол `v3-pilot-1`, один повтор, max_iterations=3. SDK gigachat 0.2.1, Python 3.14.4, Windows; прежний закреплённый Docker-образ Python 3.12.8 Alpine. Endpoint обеих моделей: `https://api.giga.chat/v1/`. Доступ к обеим моделям подтверждён списком моделей и фактическими ответами. Отдельно согласованный пользователем лимит max_tokens=4096 одинаков для моделей; n=1, stream=false, остальные настройки генерации по умолчанию. Это явно задокументированное отклонение от первоначального provider-default протокола. Все ответы завершились finish_reason=stop; обрезаний не было.','',
           'Проверки: 39 исходных offline/Docker-тестов v2 прошли; 15 новых runner/ledger-тестов и 2 теста подготовки v3 прошли. Проверены все 18 комбинаций с фикстурными ответами, разделение private held-out и development, сохранение CSV/манифеста, восстановление CSV после коммита SQLite, повторное чтение ответа без отправки, pending/unknown после сбоя, конкурентные соединения, дубликат пилота, изменение prompt hash, пропуски/несогласованность usage и кэшированный вход. Фикстурные проверки не являются API-экспериментами и не входят в результаты ниже.','',
           '## Фактический расход и результаты','',
           'В данном API usage.prompt_tokens и usage.total_tokens отражают расход после исключения кэшированного входа; полный usage сохранён. Ниже показаны и итог провайдера, и более консервативный бюджетный расход, который дополнительно включает precached_prompt_tokens. Кэш не вычитается повторно.','',
           '| Модель | Вход usage | Кэшированный вход | Выход | Итого usage | Бюджет с кэшем | Вызовы | Успех | Время оценок, с |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for model in manifest['requested_models']:
        group=[r for r in rows if r['model']==model]
        summed=lambda k:sum(int(r[k]) for r in group)
        lines.append(f"| {model} | {summed('input_tokens')} | {summed('cached_input_tokens')} | {summed('output_tokens')} | {summed('total_tokens')} | {summed('combined_budget_tokens')} | {summed('llm_calls')} | {sum(r['status']=='passed' for r in group)}/9 | {sum(float(r['elapsed_seconds']) for r in group):.2f} |")
    lines+=['',f'Общий итог usage: **{provider_total}**; бюджетный расход с кэшем: **{total}**. Разрешённый потолок: 1 000 000, целевой предел: 850 000. Остаток потолка **{1000000-total}**, остаток целевого бюджета **{850000-total}**. Неразрешённых запросов и текущих резервов нет.','',
            'Возвращённые идентификаторы модели:']
    for model,returned in sorted({(c['model'],c['returned_model']) for c in calls}):
        lines.append(f'- Запрошено `{model}`, провайдер вернул `{returned}`.')
    lines+=['','Все 18 оценок (E — easy, M — medium, H — hard; latency — суммарное время API-генерации на стороне клиента):','',
            '| Модель | Архитектура | Задача / сложность | Вход usage | Выход | Итого usage | С кэшем | LLM вызовы | Latency, с | Время оценки, с | Статус |',
            '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['model']} | {r['architecture']} | {r['task_id']} / {r['difficulty']} | {r['input_tokens']} | {r['output_tokens']} | {r['total_tokens']} | {r['combined_budget_tokens']} | {r['llm_calls']} | {r['provider_latency_seconds']:.2f} | {float(r['elapsed_seconds']):.2f} | {r['status']} |")
    lines+=['','Ошибки: Lite — 7 failed_tests, Ultra — 1 failed_tests. Инфраструктурных, аутентификационных и provider_error не зарегистрировано. Пропусков usage нет; вход usage + выход = total usage для всех 74 ответов. Успех означает прохождение held-out набора. Индивидуальных повторов для улучшения результатов не было.','',
            '## Прогнозы бюджета','',
            'В каждой из шести пар модель–архитектура измерена одна задача каждой сложности. Для одного полного повтора применена заранее заданная формула Σ(4×easy + 8×medium + 8×hard). Основной прогноз использует полный вход с кэшем и выход. Дополнительно показан аналогичный прогноз total usage. Консервативный план = фактический пилот + 1,5×прогноз main + 69 632 на один последовательно исполняемый запрос. Это плановый запас, не статистический доверительный интервал.','',
            '| Равные повторы всех 120 комбинаций | Main: usage прогноз | Main: с кэшем прогноз | Пилот + main×1,5 + резерв | Укладывается в 850 000 |',
            '|---:|---:|---:|---:|---|']
    for f in forecasts:
        lines.append(f"| {f['repeats']} | {f['main_provider_total']} | {f['main_tokens']} | {f['pilot_plus_50pct_margin_plus_reservation']} | {'да' if f['pilot_plus_50pct_margin_plus_reservation']<=850000 else 'нет'} |")
    lines+=['',f'Рекомендация: **{recommendation} сбалансированный повтор** для обеих моделей, всех трёх архитектур и всех 20 задач — 120 main-оценок. Это рекомендация для отдельного одобрения, не выполненный эксперимент. Более дорогие ячейки и трудные задачи не исключаются.','',
            '## Учёт, восстановление и ограничения','',
            'Общий SQLite WAL-журнал с synchronous=FULL фиксирует резерв до отправки, полный ответ и usage — до следующего запроса. Уникальный ключ evaluation+ordinal и хеш prompt защищают от повторной отправки и дрейфа контекста. Автоматические retries SDK отключены. Уже сохранённые ответы воспроизводятся из журнала; pending/unknown после неопределённого сбоя никогда не отправляется автоматически и блокирует дальнейшие платные запросы. Готовая оценка коммитится до экспорта CSV. Есть уникальная регистрация calibration-pilot: повторный обычный запуск не создаёт ещё один платный пилот.','',
            'Первоначально счётчик пилота учитывал total usage провайдера. Итоговый аудит обнаружил кэшированный вход и консервативно усилил текущий бюджетный учёт, добавив его к расходу. Исходный код пилота сохранён в runner-source-snapshot и совпадает с хешами его манифеста. Ответы, исходные CSV и исходный манифест не переписаны. calibration-analysis.csv содержит дополнительные вычисленные поля с кэшем; текущий ledger.py учитывает их при допуске будущих запросов. После этого исправления дополнительных API-запросов не было. Снимок manifest ledger_totals.actual при завершении пилота — total usage, а не полный расход с кэшем.','',
            'Резерв одного запроса: 65 536 входных + 4 096 выходных. Текстовый сериализованный prompt ограничен 16 384 UTF-8 байтами; молчаливого усечения нет. Такой резерв опирается на byte/subword-токенизацию, ограниченный служебный framing и соблюдение max_tokens провайдером. Это предварительный запас, а не одна лишь проверка usage после ответа; он не даёт безусловной гарантии при ошибках токенизации/учёта или нарушении лимита провайдером. Все фактические входы, включая кэш, и выходы пилота проверены на соответствие резервам. Неизвестные данные никогда не заменяются нулём.','',
            'Пилот содержит по одной задаче каждой сложности: перенос стоимости на все 20 задач имеет большую неопределённость, даже с 50% запасом. По нему нельзя делать исследовательские выводы об эффективности координации или основной выборке. Известное ограничение целостности sandbox RPC сохраняется; защиты от намеренно злонамеренного кандидата не утверждается.','',
            '## Абсолютные пути','',f'- Пилот: `{folder.resolve()}`',f'- Общий журнал: `{Path(ledger_path).resolve()}`',f'- Отчёт: `{Path(report_path).resolve()}`',
            '- raw_results.csv и summary_results.csv — исходные результаты; source-manifest.json и manifest.json — ревизии и параметры; generated_solutions — все сохранённые решения.',
            '- calibration-analysis.csv и calibration-budget.json — воспроизводимый offline-анализ. Весь raw JSON каждого ответа хранится в requests.response общего журнала.']
    Path(report_path).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    db.close()
    print(json.dumps(stats,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('folder',type=Path)
    parser.add_argument('--ledger',type=Path,default=Path('research_v3/shared-budget.sqlite3'))
    parser.add_argument('--report',type=Path,default=Path('benchmark-v3-pilot-report.md'))
    args=parser.parse_args()
    analyze(args.folder,args.ledger,args.report)
