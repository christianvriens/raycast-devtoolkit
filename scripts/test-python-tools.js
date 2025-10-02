const { PythonTools } = require('../dist/src/python-tools');

(async () => {
  try {
    const jsonText = `{
  "mobile_results_menu": "Results ({{count}})",
  "example": "Parentheses (test) and newlines\nline2"
}`;
    const res = await PythonTools.formatJson(jsonText, true);
    console.log('Result:', res);
  } catch (err) {
    console.error('Error calling PythonTools:', err);
  }
})();
