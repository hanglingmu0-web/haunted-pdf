var ningyoTimer = null;
var ningyoStep = 0;
var ningyoDoc = this;
function ningyoTick(){
    try {
       var i;
       for(i=1;i<=41;i++){
          var f=ningyoDoc.getField("frame_"+(i<10?"0":"")+i);
          if(f) f.display=display.hidden;
       }
       ningyoStep=(ningyoStep+1)%48;
       var frame=(ningyoStep<7)?0:Math.min(41,Math.floor((ningyoStep-7)*41/41)+1);
       if(frame>0){
          var g=ningyoDoc.getField("frame_"+(frame<10?"0":"")+frame);
          if(g)g.display=display.visible;
       }
    } catch(e) { console.println("Ningyo error: "+e); }
}
function ningyoStart(){
  try {
    if(ningyoTimer!==null)app.clearInterval(ningyoTimer);
    ningyoStep=0;
    ningyoTimer=app.setInterval("ningyoTick()",2000);
  } catch(e){ console.println("Ningyo start error: "+e); }
}
ningyoStart();
