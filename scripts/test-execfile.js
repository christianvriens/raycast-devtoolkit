const { execFile } = require('child_process');
const path = require('path');
const python = path.join(__dirname, '..', 'python-tools', '.venv', 'bin', 'python');
const script = path.join(__dirname, '..', 'python-tools', 'devtools.py');
const jsonArg = `{
  "mobile_results_menu": "Results ({{count}})",
  "example": "Parentheses (test) and newlines\nline2"
}`;

console.log('Using python:', python);
execFile(python, [script, 'json', jsonArg, '--minify'], (err, stdout, stderr) => {
  if (err) {
    console.error('execFile error:', err);
    console.error('stderr:', stderr);
    return;
  }
  console.log('stdout:', stdout);
});
