import streamlit as st

def inject_animation_css():
    st.markdown("""
    <style>
    /* Scanner CSS */
    .loader {
      max-width: fit-content;
      color: rgb(242, 255, 240);
      font-size: 50px;
      font-family: monospace;
      position: relative;
      font-style: italic;
      font-weight: 600;
      margin: 0 auto;
    }
    .loader span {
      animation: cut 2s infinite;
      transition: 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .loader:hover {
      color: #fcffdf;
    }
    .loader::after {
      position: absolute;
      content: "";
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background-color: #ff828291;
      top: 0px;
      filter: blur(10px);
      animation: scan 2s infinite;
      left: 0;
      z-index: 0;
      transition: 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .loader::before {
      position: absolute;
      content: "";
      width: 100%;
      height: 5px;
      border-radius: 4px;
      background-color: #ff8282;
      top: 0px;
      animation: scan 2s infinite;
      left: 0;
      z-index: 1;
      filter: opacity(0.9);
      transition: 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    @keyframes scan {
      0% { top: 0px; }
      25% { top: 54px; }
      50% { top: 0px; }
      75% { top: 54px; }
    }
    @keyframes cut {
      0% { clip-path: inset(0 0 0 0); }
      25% { clip-path: inset(100% 0 0 0); }
      50% { clip-path: inset(0 0 100% 0); }
      75% { clip-path: inset(0 0 0 0); }
    }

    /* Jumping Dot Red */
    .jump-dot-red { width: 48px; height: 48px; margin: auto; position: relative; }
    .jump-dot-red:before { content: ''; width: 48px; height: 5px; background: #f0808050; position: absolute; top: 60px; left: 0; border-radius: 50%; animation: shadow-red 0.5s linear infinite; }
    .jump-dot-red:after { content: ''; width: 100%; height: 100%; background: #f08080; position: absolute; top: 0; left: 0; border-radius: 4px; animation: jump-red 0.5s linear infinite; }
    @keyframes jump-red { 15% { border-bottom-right-radius: 3px; } 25% { transform: translateY(9px) rotate(22.5deg); } 50% { transform: translateY(18px) scale(1, .9) rotate(45deg); border-bottom-right-radius: 40px; } 75% { transform: translateY(9px) rotate(67.5deg); } 100% { transform: translateY(0) rotate(90deg); } }
    @keyframes shadow-red { 0%, 100% { transform: scale(1, 1); } 50% { transform: scale(1.2, 1); } }

    /* Jumping Dot Gold */
    .jump-dot-gold { width: 48px; height: 48px; margin: auto; position: relative; }
    .jump-dot-gold:before { content: ''; width: 48px; height: 5px; background: #FFD700; position: absolute; top: 60px; left: 0; border-radius: 50%; animation: shadow-gold 0.5s linear infinite; animation-delay: 0.15s; }
    .jump-dot-gold:after { content: ''; width: 100%; height: 100%; background: #FFD700; position: absolute; top: 0; left: 0; border-radius: 50%; animation: jump-gold 0.5s linear infinite; animation-delay: 0.15s; }
    @keyframes jump-gold { 15% { border-bottom-right-radius: 50%; } 25% { transform: translateY(9px) rotate(22.5deg); } 50% { transform: translateY(18px) scale(1, .9) rotate(45deg); border-bottom-right-radius: 40px; } 75% { transform: translateY(9px) rotate(67.5deg); } 100% { transform: translateY(0) rotate(90deg); } }
    @keyframes shadow-gold { 0%, 100% { transform: scale(1, 1); } 50% { transform: scale(1.2, 1); } }

    /* Jumping Dot Blue */
    .jump-dot-blue { width: 48px; height: 48px; margin: auto; position: relative; }
    .jump-dot-blue:before { content: ''; width: 48px; height: 5px; background: #999; position: absolute; top: 60px; left: 0; border-radius: 50%; animation: shadow-blue 0.5s linear infinite; animation-delay: 0.3s; }
    .jump-dot-blue:after { content: ''; width: 100%; height: 100%; background: rgb(61, 106, 255); position: absolute; top: 0; left: 0; border-radius: 4px; animation: jump-blue 0.5s linear infinite; animation-delay: 0.3s; }
    @keyframes jump-blue { 15% { border-bottom-right-radius: 3px; } 25% { transform: translateY(9px) rotate(22.5deg); } 50% { transform: translateY(18px) scale(1, .9) rotate(45deg); border-bottom-right-radius: 40px; } 75% { transform: translateY(9px) rotate(67.5deg); } 100% { transform: translateY(0) rotate(90deg); } }
    @keyframes shadow-blue { 0%, 100% { transform: scale(1, 1); } 50% { transform: scale(1.2, 1); } }

    /* Typewriter CSS */
    .typewriter { --blue: #5C86FF; --blue-dark: #275EFE; --key: #fff; --paper: #EEF0FD; --text: #D3D4EC; --tool: #FBC56C; --duration: 3s; position: relative; animation: bounce05 var(--duration) linear infinite; transform: scale(1.5); }
    .typewriter .slide { width: 92px; height: 20px; border-radius: 3px; margin-left: 14px; transform: translateX(14px); background: linear-gradient(var(--blue), var(--blue-dark)); animation: slide05 var(--duration) ease infinite; }
    .typewriter .slide:before, .typewriter .slide:after, .typewriter .slide i:before { content: ""; position: absolute; background: var(--tool); }
    .typewriter .slide:before { width: 2px; height: 8px; top: 6px; left: 100%; }
    .typewriter .slide:after { left: 94px; top: 3px; height: 14px; width: 6px; border-radius: 3px; }
    .typewriter .slide i { display: block; position: absolute; right: 100%; width: 6px; height: 4px; top: 4px; background: var(--tool); }
    .typewriter .slide i:before { right: 100%; top: -2px; width: 4px; border-radius: 2px; height: 14px; }
    .typewriter .paper { position: absolute; left: 24px; top: -26px; width: 40px; height: 46px; border-radius: 5px; background: var(--paper); transform: translateY(46px); animation: paper05 var(--duration) linear infinite; }
    .typewriter .paper:before { content: ""; position: absolute; left: 6px; right: 6px; top: 7px; border-radius: 2px; height: 4px; transform: scaleY(0.8); background: var(--text); box-shadow: 0 12px 0 var(--text), 0 24px 0 var(--text), 0 36px 0 var(--text); }
    .typewriter .keyboard { width: 120px; height: 56px; margin-top: -10px; z-index: 1; position: relative; }
    .typewriter .keyboard:before, .typewriter .keyboard:after { content: ""; position: absolute; }
    .typewriter .keyboard:before { top: 0; left: 0; right: 0; bottom: 0; border-radius: 7px; background: linear-gradient(135deg, var(--blue), var(--blue-dark)); transform: perspective(10px) rotateX(2deg); transform-origin: 50% 100%; }
    .typewriter .keyboard:after { left: 2px; top: 25px; width: 11px; height: 4px; border-radius: 2px; box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); animation: keyboard05 var(--duration) linear infinite; }
    
    @keyframes bounce05 { 85%, 92%, 100% { transform: translateY(0); } 89% { transform: translateY(-4px); } 95% { transform: translateY(2px); } }
    @keyframes slide05 { 5% { transform: translateX(14px); } 15%, 30% { transform: translateX(6px); } 40%, 55% { transform: translateX(0); } 65%, 70% { transform: translateX(-4px); } 80%, 89% { transform: translateX(-12px); } 100% { transform: translateX(14px); } }
    @keyframes paper05 { 5% { transform: translateY(46px); } 20%, 30% { transform: translateY(34px); } 40%, 55% { transform: translateY(22px); } 65%, 70% { transform: translateY(10px); } 80%, 85% { transform: translateY(0); } 92%, 100% { transform: translateY(46px); } }
    @keyframes keyboard05 { 5%, 12%, 21%, 30%, 39%, 48%, 57%, 66%, 75%, 84% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 9% { box-shadow: 15px 2px 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 18% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 2px 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 27% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 12px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 36% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 12px 0 var(--key), 60px 12px 0 var(--key), 68px 12px 0 var(--key), 83px 10px 0 var(--key); } 45% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 2px 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 54% { box-shadow: 15px 0 0 var(--key), 30px 2px 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 63% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 12px 0 var(--key); } 72% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 2px 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 10px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } 81% { box-shadow: 15px 0 0 var(--key), 30px 0 0 var(--key), 45px 0 0 var(--key), 60px 0 0 var(--key), 75px 0 0 var(--key), 90px 0 0 var(--key), 22px 10px 0 var(--key), 37px 12px 0 var(--key), 52px 10px 0 var(--key), 60px 10px 0 var(--key), 68px 10px 0 var(--key), 83px 10px 0 var(--key); } }

    /* Hand CSS */
    .🤚 {
      --skin-color: #E4C560;
      --tap-speed: 0.6s;
      --tap-stagger: 0.1s;
      position: relative;
      width: 80px;
      height: 60px;
      margin: 0 auto;
    }
    .🤚:before {
      content: '';
      display: block;
      width: 180%;
      height: 75%;
      position: absolute;
      top: 70%;
      right: 20%;
      background-color: black;
      border-radius: 40px 10px;
      filter: blur(10px);
      opacity: 0.3;
    }
    .🌴 {
      display: block;
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      background-color: var(--skin-color);
      border-radius: 10px 40px;
    }
    .👍 {
      position: absolute;
      width: 120%;
      height: 38px;
      background-color: var(--skin-color);
      bottom: -18%;
      right: 1%;
      transform-origin: calc(100% - 20px) 20px;
      transform: rotate(-20deg);
      border-radius: 30px 20px 20px 10px;
      border-bottom: 2px solid rgba(0, 0, 0, 0.1);
      border-left: 2px solid rgba(0, 0, 0, 0.1);
    }
    .👍:after {
      width: 20%;
      height: 60%;
      content: '';
      background-color: rgba(255, 255, 255, 0.3);
      position: absolute;
      bottom: -8%;
      left: 5px;
      border-radius: 60% 10% 10% 30%;
      border-right: 2px solid rgba(0, 0, 0, 0.05);
    }
    .👉 {
      position: absolute;
      width: 80%;
      height: 35px;
      background-color: var(--skin-color);
      bottom: 32%;
      right: 64%;
      transform-origin: 100% 20px;
      animation-duration: calc(var(--tap-speed) * 2);
      animation-timing-function: ease-in-out;
      animation-iteration-count: infinite;
      transform: rotate(10deg);
    }
    .👉:before {
      content: '';
      position: absolute;
      width: 140%;
      height: 30px;
      background-color: var(--skin-color);
      bottom: 8%;
      right: 65%;
      transform-origin: calc(100% - 20px) 20px;
      transform: rotate(-60deg);
      border-radius: 20px;
    }
    .👉:nth-child(1) { animation-delay: 0; filter: brightness(70%); animation-name: tap-upper-1; }
    .👉:nth-child(2) { animation-delay: var(--tap-stagger); filter: brightness(80%); animation-name: tap-upper-2; }
    .👉:nth-child(3) { animation-delay: calc(var(--tap-stagger) * 2); filter: brightness(90%); animation-name: tap-upper-3; }
    .👉:nth-child(4) { animation-delay: calc(var(--tap-stagger) * 3); filter: brightness(100%); animation-name: tap-upper-4; }

    @keyframes tap-upper-1 { 0%, 50%, 100% { transform: rotate(10deg) scale(0.4); } 40% { transform: rotate(50deg) scale(0.4); } }
    @keyframes tap-upper-2 { 0%, 50%, 100% { transform: rotate(10deg) scale(0.6); } 40% { transform: rotate(50deg) scale(0.6); } }
    @keyframes tap-upper-3 { 0%, 50%, 100% { transform: rotate(10deg) scale(0.8); } 40% { transform: rotate(50deg) scale(0.8); } }
    @keyframes tap-upper-4 { 0%, 50%, 100% { transform: rotate(10deg) scale(1); } 40% { transform: rotate(50deg) scale(1); } }

    /* Hamster CSS */
    .wheel-and-hamster {
      --dur: 1s;
      position: relative;
      width: 12em;
      height: 12em;
      font-size: 14px;
      margin: 0 auto;
    }
    .wheel, .hamster, .hamster div, .spoke { position: absolute; }
    .wheel, .spoke { border-radius: 50%; top: 0; left: 0; width: 100%; height: 100%; }
    .wheel { background: radial-gradient(100% 100% at center,hsla(0,0%,60%,0) 47.8%,hsl(0,0%,60%) 48%); z-index: 2; }
    .hamster { animation: hamster var(--dur) ease-in-out infinite; top: 50%; left: calc(50% - 3.5em); width: 7em; height: 3.75em; transform: rotate(4deg) translate(-0.8em,1.85em); transform-origin: 50% 0; z-index: 1; }
    .hamster__head { animation: hamsterHead var(--dur) ease-in-out infinite; background: hsl(30,90%,55%); border-radius: 70% 30% 0 100% / 40% 25% 25% 60%; box-shadow: 0 -0.25em 0 hsl(30,90%,80%) inset, 0.75em -1.55em 0 hsl(30,90%,90%) inset; top: 0; left: -2em; width: 2.75em; height: 2.5em; transform-origin: 100% 50%; }
    .hamster__ear { animation: hamsterEar var(--dur) ease-in-out infinite; background: hsl(0,90%,85%); border-radius: 50%; box-shadow: -0.25em 0 hsl(30,90%,55%) inset; top: -0.25em; right: -0.25em; width: 0.75em; height: 0.75em; transform-origin: 50% 75%; }
    .hamster__eye { animation: hamsterEye var(--dur) linear infinite; background-color: hsl(0,0%,0%); border-radius: 50%; top: 0.375em; left: 1.25em; width: 0.5em; height: 0.5em; }
    .hamster__nose { background: hsl(0,90%,75%); border-radius: 35% 65% 85% 15% / 70% 50% 50% 30%; top: 0.75em; left: 0; width: 0.2em; height: 0.25em; }
    .hamster__body { animation: hamsterBody var(--dur) ease-in-out infinite; background: hsl(30,90%,90%); border-radius: 50% 30% 50% 30% / 15% 60% 40% 40%; box-shadow: 0.1em 0.75em 0 hsl(30,90%,55%) inset, 0.15em -0.5em 0 hsl(30,90%,80%) inset; top: 0.25em; left: 2em; width: 4.5em; height: 3em; transform-origin: 17% 50%; transform-style: preserve-3d; }
    .hamster__limb--fr, .hamster__limb--fl { clip-path: polygon(0 0,100% 0,70% 80%,60% 100%,0% 100%,40% 80%); top: 2em; left: 0.5em; width: 1em; height: 1.5em; transform-origin: 50% 0; }
    .hamster__limb--fr { animation: hamsterFRLimb var(--dur) linear infinite; background: linear-gradient(hsl(30,90%,80%) 80%,hsl(0,90%,75%) 80%); transform: rotate(15deg) translateZ(-1px); }
    .hamster__limb--fl { animation: hamsterFLLimb var(--dur) linear infinite; background: linear-gradient(hsl(30,90%,90%) 80%,hsl(0,90%,85%) 80%); transform: rotate(15deg); }
    .hamster__limb--br, .hamster__limb--bl { border-radius: 0.75em 0.75em 0 0; clip-path: polygon(0 0,100% 0,100% 30%,70% 90%,70% 100%,30% 100%,40% 90%,0% 30%); top: 1em; left: 2.8em; width: 1.5em; height: 2.5em; transform-origin: 50% 30%; }
    .hamster__limb--br { animation: hamsterBRLimb var(--dur) linear infinite; background: linear-gradient(hsl(30,90%,80%) 90%,hsl(0,90%,75%) 90%); transform: rotate(-25deg) translateZ(-1px); }
    .hamster__limb--bl { animation: hamsterBLLimb var(--dur) linear infinite; background: linear-gradient(hsl(30,90%,90%) 90%,hsl(0,90%,85%) 90%); transform: rotate(-25deg); }
    .hamster__tail { animation: hamsterTail var(--dur) linear infinite; background: hsl(0,90%,85%); border-radius: 0.25em 50% 50% 0.25em; box-shadow: 0 -0.2em 0 hsl(0,90%,75%) inset; top: 1.5em; right: -0.5em; width: 1em; height: 0.5em; transform: rotate(30deg) translateZ(-1px); transform-origin: 0.25em 0.25em; }
    .spoke { animation: spoke var(--dur) linear infinite; background: radial-gradient(100% 100% at center,hsl(0,0%,60%) 4.8%,hsla(0,0%,60%,0) 5%), linear-gradient(hsla(0,0%,55%,0) 46.9%,hsl(0,0%,65%) 47% 52.9%,hsla(0,0%,65%,0) 53%) 50% 50% / 99% 99% no-repeat; }

    @keyframes hamster { from, to { transform: rotate(4deg) translate(-0.8em,1.85em); } 50% { transform: rotate(0) translate(-0.8em,1.85em); } }
    @keyframes hamsterHead { from, 25%, 50%, 75%, to { transform: rotate(0); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(8deg); } }
    @keyframes hamsterEye { from, 90%, to { transform: scaleY(1); } 95% { transform: scaleY(0); } }
    @keyframes hamsterEar { from, 25%, 50%, 75%, to { transform: rotate(0); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(12deg); } }
    @keyframes hamsterBody { from, 25%, 50%, 75%, to { transform: rotate(0); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(-2deg); } }
    @keyframes hamsterFRLimb { from, 25%, 50%, 75%, to { transform: rotate(50deg) translateZ(-1px); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(-30deg) translateZ(-1px); } }
    @keyframes hamsterFLLimb { from, 25%, 50%, 75%, to { transform: rotate(-30deg); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(50deg); } }
    @keyframes hamsterBRLimb { from, 25%, 50%, 75%, to { transform: rotate(-60deg) translateZ(-1px); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(20deg) translateZ(-1px); } }
    @keyframes hamsterBLLimb { from, 25%, 50%, 75%, to { transform: rotate(20deg); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(-60deg); } }
    @keyframes hamsterTail { from, 25%, 50%, 75%, to { transform: rotate(30deg) translateZ(-1px); } 12.5%, 37.5%, 62.5%, 87.5% { transform: rotate(10deg) translateZ(-1px); } }
    @keyframes spoke { from { transform: rotate(0); } to { transform: rotate(-1turn); } }

    /* Alternator CSS */
    .animation-wrapper {
        position: relative;
        height: 200px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .anim-hand {
        position: absolute;
        animation: fade1 12s infinite;
    }
    .anim-hamster {
        position: absolute;
        animation: fade2 12s infinite;
    }
    .anim-typewriter {
        position: absolute;
        animation: fade3 12s infinite;
    }
    @keyframes fade1 {
        0%, 30% { opacity: 1; visibility: visible; }
        35%, 100% { opacity: 0; visibility: hidden; }
    }
    @keyframes fade2 {
        0%, 30% { opacity: 0; visibility: hidden; }
        35%, 63% { opacity: 1; visibility: visible; }
        68%, 100% { opacity: 0; visibility: hidden; }
    }
    @keyframes fade3 {
        0%, 63% { opacity: 0; visibility: hidden; }
        68%, 95% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }
    </style>
    """, unsafe_allow_html=True)

def render_scanner():
    return """
    <div style="display: flex; justify-content: center; align-items: center; gap: 4rem; padding: 2rem;">
        <div class="jump-dot-red"></div>
        <div class="jump-dot-gold"></div>
        <div class="jump-dot-blue"></div>
    </div>
    """

def render_alternating_animations():
    return """
    <div class="animation-wrapper">
        <div class="anim-hand">
            <div class="🤚">
              <div class="👉"></div>
              <div class="👉"></div>
              <div class="👉"></div>
              <div class="👉"></div>
              <div class="🌴"></div>
              <div class="👍"></div>
            </div>
        </div>
        <div class="anim-hamster">
            <div aria-label="Orange and tan hamster running in a metal wheel" role="img" class="wheel-and-hamster">
              <div class="wheel"></div>
              <div class="hamster">
                <div class="hamster__body">
                  <div class="hamster__head">
                    <div class="hamster__ear"></div>
                    <div class="hamster__eye"></div>
                    <div class="hamster__nose"></div>
                  </div>
                  <div class="hamster__limb hamster__limb--fr"></div>
                  <div class="hamster__limb hamster__limb--fl"></div>
                  <div class="hamster__limb hamster__limb--br"></div>
                  <div class="hamster__limb hamster__limb--bl"></div>
                  <div class="hamster__tail"></div>
                </div>
              </div>
              <div class="spoke"></div>
            </div>
        </div>
        <div class="anim-typewriter">
            <div class="typewriter">
                <div class="slide"><i></i></div>
                <div class="paper"></div>
                <div class="keyboard"></div>
            </div>
        </div>
    </div>
    """


def inject_custom_fact_check_button():
    import streamlit.components.v1 as components
    components.html("""
    <script>
    const parentDoc = window.parent.document;
    
    // Inject the CSS
    if (!parentDoc.getElementById('custom-fc-btn-css')) {
        const style = parentDoc.createElement('style');
        style.id = 'custom-fc-btn-css';
        style.innerHTML = `
        .custom-magic-btn {
          --black-700: hsla(0 0% 12% / 1);
          --border_radius: 9999px;
          --transtion: 0.3s ease-in-out;
          --offset: 2px;
        
          cursor: pointer !important;
          position: relative !important;
        
          display: flex !important;
          align-items: center !important;
          gap: 0.5rem !important;
        
          transform-origin: center !important;
        
          padding: 1rem 2rem !important;
          background-color: transparent !important;
        
          border: none !important;
          border-radius: var(--border_radius) !important;
          transform: scale(calc(1 + (var(--active, 0) * 0.1))) !important;
        
          transition: transform var(--transtion) !important;
          width: 100% !important;
          justify-content: center !important;
        }
        
        .custom-magic-btn::before {
          content: "";
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        
          width: 100%;
          height: 100%;
          background-color: var(--black-700);
        
          border-radius: var(--border_radius);
          box-shadow: inset 0 0.5px hsl(0, 0%, 100%), inset 0 -1px 2px 0 hsl(0, 0%, 0%),
            0px 4px 10px -4px hsla(0 0% 0% / calc(1 - var(--active, 0))),
            0 0 0 calc(var(--active, 0) * 0.375rem) hsl(260 97% 50% / 0.75);
        
          transition: all var(--transtion);
          z-index: 0;
        }
        
        .custom-magic-btn::after {
          content: "";
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        
          width: 100%;
          height: 100%;
          background-color: hsla(260 97% 61% / 0.75);
          background-image: radial-gradient(
              at 51% 89%,
              hsla(266, 45%, 74%, 1) 0px,
              transparent 50%
            ),
            radial-gradient(at 100% 100%, hsla(266, 36%, 60%, 1) 0px, transparent 50%),
            radial-gradient(at 22% 91%, hsla(266, 36%, 60%, 1) 0px, transparent 50%);
          background-position: top;
        
          opacity: var(--active, 0);
          border-radius: var(--border_radius);
          transition: opacity var(--transtion);
          z-index: 2;
        }
        
        .custom-magic-btn:is(:hover, :focus-visible) {
          --active: 1;
        }
        .custom-magic-btn:active {
          transform: scale(1) !important;
        }
        
        .custom-magic-btn .dots_border {
          --size_border: calc(100% + 2px);
        
          overflow: hidden;
        
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        
          width: var(--size_border);
          height: var(--size_border);
          background-color: transparent;
        
          border-radius: var(--border_radius);
          z-index: -10;
        }
        
        .custom-magic-btn .dots_border::before {
          content: "";
          position: absolute;
          top: 30%;
          left: 50%;
          transform: translate(-50%, -50%);
          transform-origin: left;
          transform: rotate(0deg);
        
          width: 100%;
          height: 2rem;
          background-color: white;
        
          mask: linear-gradient(transparent 0%, white 120%);
          -webkit-mask: linear-gradient(transparent 0%, white 120%);
          animation: rotate 2s linear infinite;
        }
        
        @keyframes rotate {
          to {
            transform: rotate(360deg);
          }
        }
        
        .custom-magic-btn .sparkle {
          position: relative;
          z-index: 10;
          width: 1.75rem;
        }
        
        .custom-magic-btn .sparkle .path {
          fill: currentColor;
          stroke: currentColor;
          transform-origin: center;
          color: hsl(0, 0%, 100%);
        }
        
        .custom-magic-btn:is(:hover, :focus) .sparkle .path {
          animation: path 1.5s linear 0.5s infinite;
        }
        
        .custom-magic-btn .sparkle .path:nth-child(1) {
          --scale_path_1: 1.2;
        }
        .custom-magic-btn .sparkle .path:nth-child(2) {
          --scale_path_2: 1.2;
        }
        .custom-magic-btn .sparkle .path:nth-child(3) {
          --scale_path_3: 1.2;
        }
        
        @keyframes path {
          0%,
          34%,
          71%,
          100% {
            transform: scale(1);
          }
          17% {
            transform: scale(var(--scale_path_1, 1));
          }
          49% {
            transform: scale(var(--scale_path_2, 1));
          }
          83% {
            transform: scale(var(--scale_path_3, 1));
          }
        }
        
        .custom-magic-btn .text_button {
          position: relative;
          z-index: 10;
        
          background-image: linear-gradient(
            90deg,
            hsla(0 0% 100% / 1) 0%,
            hsla(0 0% 100% / var(--active, 0)) 120%
          );
          background-clip: text;
          -webkit-background-clip: text;
          font-size: 1.2rem;
          color: transparent !important;
          font-weight: bold;
        }
        `;
        parentDoc.head.appendChild(style);
    }
    
    // Find the Streamlit button
    const interval = setInterval(() => {
        const buttons = Array.from(parentDoc.querySelectorAll('button'));
        const targetBtn = buttons.find(b => b.textContent && b.textContent.includes('Start Fact-Check Analysis'));
        
        if (targetBtn && !targetBtn.hasAttribute('data-customized')) {
            targetBtn.setAttribute('data-customized', 'true');
            targetBtn.className = targetBtn.className + ' custom-magic-btn';
            
            targetBtn.innerHTML = `
              <div class="dots_border"></div>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="sparkle">
                <path class="path" d="M10,21.236,6.755,14.745.264,11.5,6.755,8.255,10,1.764l3.245,6.491L19.736,11.5l-6.491,3.245Z" />
                <path class="path" d="M18,21l1.5,3L21,21l3-1.5L21,18l-1.5-3L18,18l-3,1.5Z" />
                <path class="path" d="M19.333,4.667,20.5,7l1.167-2.333L24,3.5,21.667,2.333,20.5,0,19.333,2.333,17,3.5Z" />
              </svg>
              <span class="text_button">Start Fact-Check Analysis</span>
            `;
            clearInterval(interval);
        }
    }, 100);
    </script>
    """, height=0, width=0)
