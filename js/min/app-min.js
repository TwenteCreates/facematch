var brfv4Example={appId:"facematch",loader:{queuePreloader:null},imageData:{webcam:{stream:null},picture:{}},dom:{},gui:{},drawing:{},drawing3d:{t3d:{}},stats:{}},brfv4={locateFile:function(e){return"js/libs/brf/BRFv4_JS_trial.js.mem"}};brfv4Example.start=function(){brfv4Example.loader.preload(["js/libs/brf/BRFv4_JS_trial.js","https://webrtc.github.io/adapter/adapter-latest.js","js/libs/quicksettings/quicksettings.min.css","js/libs/quicksettings/quicksettings.js","js/libs/createjs/easeljs-0.8.2.min.js","js/libs/threejs/three.js","js/utils/BRFv4DOMUtils.js","js/utils/BRFv4DrawingUtils_CreateJS.js","js/utils/BRFv4Drawing3DUtils_ThreeJS.js","js/utils/BRFv4SetupWebcam.js","js/utils/BRFv4SetupPicture.js","js/utils/BRFv4SetupExample.js","js/utils/BRFv4PointUtils.js"],function(){brfv4Example.init("webcam")})},brfv4Example.trace=function(e,t){if("undefined"!=typeof window&&window.console){var s=(window.performance.now()/1e3).toFixed(3);t?window.console.error(s+": ",e):window.console.log(s+": ",e)}},function(){"use strict";var e=brfv4Example.loader;e.preload=function(t,s){function n(e){}function a(e){s&&s()}if(null===e.queuePreloader&&t){var i=e.queuePreloader=new createjs.LoadQueue(!0);i.on("progress",n),i.on("complete",a),i.loadManifest(t,!0)}},e.loadExample=function(t,s){function n(e){s&&s()}var a=e.queueExamples=new createjs.LoadQueue(!0);a.on("progress",onProgress),a.on("complete",n),a.loadManifest(t,!0)}}(),function e(){"use strict";brfv4Example.initCurrentExample=function(e,t){e.init(t,t,brfv4Example.appId)},brfv4Example.updateCurrentExample=function(e,t,s){e.update(t),s.clear();for(var n=e.getFaces(),a=0;a<n.length;a++){var i=n[a];"state_face_detection"===i.state&&(document.querySelector(".facebox").style.display="none",document.querySelector(".infofacebox").style.display="none");var o=document.querySelector(".facebox-"+a);o||(o=document.createElement("div"),o.classList.add("facebox"),o.classList.add("facebox-"+a),document.body.appendChild(o)),o.style.left=document.querySelector("#_drawing").getBoundingClientRect().x+i.bounds.x-50+"px",o.style.top=document.querySelector("#_drawing").getBoundingClientRect().y+i.bounds.y-50+"px",o.style.height=i.bounds.height-50+"px",o.style.width=i.bounds.width-50+"px",o.style.display="block";var r=document.querySelector(".infofacebox-"+a);r||(r=document.createElement("div"),r.classList.add("infofacebox"),r.classList.add("infofacebox-"+a),document.body.appendChild(r)),r.innerHTML="Name: Sample Name<br>Age: 23&ndash;30",r.style.left=document.querySelector("#_drawing").getBoundingClientRect().x+i.bounds.x+i.bounds.width+50+"px",r.style.top=document.querySelector("#_drawing").getBoundingClientRect().y+i.bounds.y+"px",r.style.display="block",i.state!==brfv4.BRFState.FACE_TRACKING_START&&i.state!==brfv4.BRFState.FACE_TRACKING||(s.drawTriangles(i.vertices,i.triangles,!1,.5,41215,.35),s.drawVertices(i.vertices,1.5,!1,41215,.5))}}}(),window.onload=brfv4Example.start;