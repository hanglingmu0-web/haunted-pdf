// Only run against the reviewed sample scripts. A Node vm is not a security boundary.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const results = [];
for (const name of ['snow', 'ningyo-animation']) {
  const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, '../work/validation', name+'-js.json'), 'utf8'));
  const fields = Object.fromEntries(Array.from({length:41}, (_,i) => ['frame_'+String(i+1).padStart(2,'0'), {display:1}]));
  let nextTimer=0;
  const timers=new Map();
  const context=vm.createContext({
    display:{visible:0, hidden:1, noPrint:2, noView:3},
    getField(name) { assert.ok(fields[name]); return fields[name]; },
    console:{println(message) { throw new Error(message); }},
    app:{
      setInterval(code, ms) { assert.equal(ms, fixture.interval); const id=++nextTimer; timers.set(id,code); return id; },
      clearInterval(id) { assert.ok(timers.delete(id)); },
    },
  });
  vm.runInContext(fixture.main, context, {timeout:1000});
  assert.equal(timers.size,1, 'document-level script auto-starts');
  vm.runInContext(fixture.open, context, {timeout:1000});
  assert.equal(timers.size,1, 'OpenAction replaces rather than duplicates timer');
  const visible = () => Object.entries(fields).filter(([,v])=>v.display===0).map(([k])=>Number(k.slice(-2)));
  assert.deepEqual(visible(),[]);
  for(let tick=1; tick<=144; tick++) {
    vm.runInContext([...timers.values()][0],context,{timeout:1000});
    const step=tick%48;
    assert.deepEqual(visible(),step<7 ? [] : [step-6], 'frame order at tick '+tick);
  }
  results.push({sample:name, ticks:144, loops:3, interval_ms:fixture.interval,
    first_widget_ms:7*fixture.interval, cycle_ms:48*fixture.interval, status:'pass',
    scope:'mock Acrobat APIs; not a viewer playback test'});
}
console.log(JSON.stringify(results,null,2));
