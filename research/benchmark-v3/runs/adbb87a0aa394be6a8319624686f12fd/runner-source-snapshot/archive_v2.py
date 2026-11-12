"""Make a byte-preserving local archive. No credentials, APIs or Git mutations."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
V2 = Path(r'multiagent_llm_experiment')
IDS = ['a53ee08c98454e7897829907549410b6','1a63bfbd0c8b4b4dabe26bfd6bc12eeb',
       '492011404d80499bae114be267f27d15','68f88919d96b4b919934a43566035a59']


def main():
    destination = ROOT/'research_archive'
    destination.mkdir(exist_ok=True)
    archive = destination/'benchmark-v2-originals.zip'
    if archive.exists():
        raise SystemExit('Archive exists; refusing to overwrite.')
    files = {}
    for ident in IDS:
        folder = V2/'runs'/ident
        for name in ['raw_results.csv','summary_results.csv','manifest.json']:
            if not (folder/name).is_file():
                raise SystemExit(f'Missing original {ident}/{name}; no synthetic replacement allowed')
        for p in folder.rglob('*'):
            if p.is_file():
                files['benchmark_v2/runs/'+ident+'/'+p.relative_to(folder).as_posix()] = p
    for p in (ROOT/'lite-benchmark-work').glob('*.py'):
        files['benchmark_v2/lite_source_snapshot/'+p.name] = p
    for p in V2.glob('*.py'):
        files['benchmark_v2/current_matching_source/'+p.name] = p
    for name in ['requirements.txt']:
        files['benchmark_v2/current_matching_source/'+name] = V2/name
    for name in ['lite-benchmark-report.md','ultra-benchmark-report.md','ultra-full-usage-monitor.csv','ultra-budget-runner.py']:
        files['benchmark_v2/reports_and_limitations/'+name] = ROOT/name
    # Legacy/publication-era data are separate, with their original labels.
    # Archival provenance is not independent validation of publication claims.
    legacy=ROOT/'multiagent_llm_experiment'
    for folder_name in ['results','results_check','generated_solutions']:
        folder=legacy/folder_name
        if folder.exists():
            for p in folder.rglob('*'):
                if p.is_file() and p.suffix in {'.csv','.json','.py','.md'}:
                    files['historical_unverified/'+folder_name+'/'+p.relative_to(folder).as_posix()]=p
    index=[]
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,p in sorted(files.items()):
            data=p.read_bytes()
            z.writestr(name,data)
            index.append({'entry':name,'original_path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    with zipfile.ZipFile(archive) as z:
        for entry in index:
            assert hashlib.sha256(z.read(entry['entry'])).hexdigest()==entry['sha256']
            assert hashlib.sha256(Path(entry['original_path']).read_bytes()).hexdigest()==entry['sha256']
    output={'archive':str(archive),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'verified_original_bytes':True,'benchmark_v2_experiment_ids':IDS,
            'historical_provenance':'Unverified legacy files; no reconstruction or reassessment of missing publication records.',
            'limitation':'Known adversarial RPC integrity limitation remains; sandbox is not claimed secure against malicious candidates.',
            'files':index}
    (destination/'archive-index.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Archived and byte-verified {len(index)} original files.')


if __name__=='__main__':
    main()
