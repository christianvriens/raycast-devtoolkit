const { spawn, execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

function getPythonToolsPath() {
  const possible = [
    path.join(__dirname, '..', 'python-tools', 'devtools.py'),
  ];
  for (const p of possible) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error('devtools.py not found');
}

const PY = getPythonToolsPath();
const venvPython = path.join(path.dirname(PY), '.venv', 'bin', 'python');
const pythonBin = fs.existsSync(venvPython) ? venvPython : 'python3';
console.log('Using Python tools at', PY, 'with interpreter', pythonBin);

function runJson(text, minify = false) {
  return new Promise((resolve, reject) => {
    const args = ['json', '-'];
    if (minify) args.push('--minify');
  const proc = spawn(pythonBin, [PY, ...args]);
    let out = '';
    let err = '';
    proc.stdout.on('data', d => out += d.toString());
    proc.stderr.on('data', d => err += d.toString());
    proc.on('close', (code) => {
      if (err) return reject(new Error(err));
      try { resolve(JSON.parse(out)); } catch (e) { reject(e); }
    });
    proc.stdin.write(text);
    proc.stdin.end();
  });
}

function runEscape(text, operation = 'escape', format = 'html') {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ text, operation, format });
    execFile(pythonBin, [PY, 'run', 'escape', payload], (err, stdout, stderr) => {
      if (err) return reject(err);
      if (stderr && stderr.trim().length > 0) {
        console.error('escape stderr:', stderr);
        return reject(new Error(stderr));
      }
      try { resolve(JSON.parse(stdout)); } catch (e) { 
        console.error('escape raw stdout:', stdout);
        return reject(e);
      }
    });
  });
}

function runBase64(text, decode=false) {
  return new Promise((resolve, reject) => {
    const args = ['base64', text];
    if (decode) args.push('--decode');
  execFile(pythonBin, [PY, ...args], (err, stdout, stderr) => {
      if (err) return reject(err);
      if (stderr) return reject(new Error(stderr));
      try { resolve(JSON.parse(stdout)); } catch (e) { reject(e); }
    });
  });
}

function runUrl(text, decode=false) {
  return new Promise((resolve, reject) => {
    const args = ['url', text];
    if (decode) args.push('--decode');
  execFile(pythonBin, [PY, ...args], (err, stdout, stderr) => {
      if (err) return reject(err);
      if (stderr) return reject(new Error(stderr));
      try { resolve(JSON.parse(stdout)); } catch (e) { reject(e); }
    });
  });
}

function runHash(text, algo='sha256') {
  return new Promise((resolve, reject) => {
  execFile(pythonBin, [PY, 'hash', text, '--algorithm', algo], (err, stdout, stderr) => {
      if (err) return reject(err);
      if (stderr) return reject(new Error(stderr));
      try { resolve(JSON.parse(stdout)); } catch (e) { reject(e); }
    });
  });
}

(async function() {
  try {
    console.log('JSON pretty:');
    const pretty = await runJson('{"a":1,"b":[1,2,3]}', false);
    console.log(pretty);

    console.log('JSON minify:');
    const min = await runJson('{\n  "a": 1,\n  "b": [1,2,3]\n}\n', true);
    console.log(min);

    console.log('Escape HTML:');
    const esc = await runEscape('<div>"Hello" & test</div>', 'escape', 'html');
    console.log(esc);

    console.log('Unescape HTML:');
    const unesc = await runEscape('&lt;div&gt;&quot;Hello&quot; &amp; test&lt;/div&gt;', 'unescape', 'html');
    console.log(unesc);

    console.log('Base64 encode:');
    const b = await runBase64('hello world', false);
    console.log(b);

    console.log('URL encode:');
    const u = await runUrl('https://example.com/?q=one two', false);
    console.log(u);

    console.log('Hash (sha256):');
    const h = await runHash('hello world', 'sha256');
    console.log(h);

    console.log('All smoke tests completed successfully');
  } catch (e) {
    console.error('Smoke test failed:', e && (e.message || e));
    process.exit(1);
  }
})();
