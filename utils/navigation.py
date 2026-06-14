import streamlit as st

def render_theme_toggle():
    import streamlit.components.v1 as components
    components.html("""
    <script>
    const parentDoc = window.parent.document;
    
    // Inject Theme Toggle Button if not exists
    if (!parentDoc.getElementById('custom-theme-toggle-wrapper')) {
        const toggleWrapper = parentDoc.createElement('div');
        toggleWrapper.id = 'custom-theme-toggle-wrapper';
        toggleWrapper.style.position = 'fixed';
        toggleWrapper.style.top = '1rem';
        toggleWrapper.style.right = '4rem';
        toggleWrapper.style.zIndex = '999999';
        
        toggleWrapper.innerHTML = `
        <label class="theme-switch">
          <!-- Checked by default = Night/Dark Mode -->
          <input type="checkbox" class="theme-switch__checkbox" checked>
          <div class="theme-switch__container">
            <div class="theme-switch__stars-container">
              <div class="theme-switch__stars-cluster">
                <div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div>
              </div>
              <div class="theme-switch__shooting-star"></div>
              <div class="theme-switch__shooting-star-2"></div>
              <div class="theme-switch__meteor"></div>
              <div class="theme-switch__aurora"></div>
              <div class="theme-switch__comets">
                <div class="comet"></div><div class="comet"></div>
              </div>
            </div>
            <div class="theme-switch__circle-container">
              <div class="theme-switch__sun-moon-container">
                <div class="theme-switch__moon">
                  <div class="theme-switch__spot"></div>
                  <div class="theme-switch__spot"></div>
                  <div class="theme-switch__spot"></div>
                </div>
              </div>
            </div>
            <div class="theme-switch__clouds"></div>
          </div>
        </label>
        `;
        
        // CSS for toggle and light mode
        const style = parentDoc.createElement('style');
        style.innerHTML = `
        /* ─── Theme Toggle CSS ─── */
        .theme-switch {
          --toggle-size: 16px;
          --container-width: 5.625em;
          --container-height: 2.5em;
          --container-radius: 0.38em;
          --container-light-bg: #5caad4;
          --container-night-bg: #1b1e36;
          --circle-container-diameter: 3.375em;
          --sun-moon-diameter: 2.125em;
          --sun-bg: #f5c518;
          --moon-bg: #d8d4c0;
          --spot-color: #9b9787;
          --circle-container-offset: calc((var(--circle-container-diameter) - var(--container-height)) / 2 * -1);
          --stars-color: #fff8e1;
          --clouds-color: #f4f4f4;
          --back-clouds-color: #bacfe0;
          --transition: 0.5s cubic-bezier(0, -0.02, 0.4, 1.25);
          --circle-transition: 0.3s cubic-bezier(0, -0.02, 0.35, 1.17);
          display: inline-block;
        }
        .theme-switch, .theme-switch *, .theme-switch *::before, .theme-switch *::after {
          box-sizing: border-box; margin: 0; padding: 0; font-size: var(--toggle-size);
        }
        .theme-switch__container {
          width: var(--container-width); height: var(--container-height);
          background-color: var(--container-light-bg); border-radius: var(--container-radius);
          overflow: hidden; cursor: pointer; position: relative;
          background-image: linear-gradient(to bottom, var(--container-light-bg) 0%, #4a92bd 100%);
          transition: all var(--transition);
          box-shadow: 0 0 0 2.5px #1a1a1a, 3px 4px 0 2.5px rgba(26, 26, 26, 0.22);
          transform: rotate(-0.7deg);
        }
        .theme-switch__checkbox { display: none; }
        .theme-switch__circle-container {
          width: var(--circle-container-diameter); height: var(--circle-container-diameter);
          background-color: rgba(255, 255, 255, 0.1); position: absolute;
          left: var(--circle-container-offset); top: var(--circle-container-offset);
          border-radius: var(--container-radius);
          box-shadow: inset 0 0 0 3.375em rgba(255, 255, 255, 0.1), inset 0 0 0 3.375em rgba(255, 255, 255, 0.1), 0 0 0 0.625em rgba(255, 255, 255, 0.1), 0 0 0 1.25em rgba(255, 255, 255, 0.1);
          display: flex; transition: var(--circle-transition); pointer-events: none;
        }
        .theme-switch__sun-moon-container {
          pointer-events: auto; position: relative; z-index: 2;
          width: var(--sun-moon-diameter); height: var(--sun-moon-diameter);
          margin: auto; border-radius: var(--container-radius); background-color: var(--sun-bg);
          box-shadow: 0.062em 0.062em 0.062em 0em rgba(254, 255, 239, 0.61) inset, 0em -0.062em 0.062em 0em #a1872a inset, 0.1em 0.13em 0 0.04em #1a1a1a;
          overflow: hidden; transition: var(--transition); transform: scale(1);
        }
        .theme-switch__moon {
          transform: translateX(100%); width: 100%; height: 100%;
          background-color: var(--moon-bg); border-radius: inherit;
          box-shadow: 0.062em 0.062em 0.062em 0em rgba(254, 255, 239, 0.61) inset, 0em -0.062em 0.062em 0em #969696 inset;
          transition: all var(--transition), transform 0.3s ease; position: relative;
        }
        .theme-switch__spot {
          position: absolute; top: 0.75em; left: 0.312em; width: 0.75em; height: 0.75em;
          border-radius: var(--container-radius); background-color: var(--spot-color);
          box-shadow: 0em 0.0312em 0.062em rgba(0, 0, 0, 0.25) inset;
          transition: background-color 0.3s ease;
        }
        .theme-switch__spot:nth-of-type(2) { width: 0.375em; height: 0.375em; top: 0.937em; left: 1.375em; }
        .theme-switch__spot:nth-last-of-type(3) { width: 0.25em; height: 0.25em; top: 0.312em; left: 0.812em; }
        .theme-switch__clouds {
          width: 1.25em; height: 1.25em; background-color: var(--clouds-color);
          border-radius: var(--container-radius); position: absolute; bottom: -0.625em; left: 0.312em;
          box-shadow: 0.937em 0.312em var(--clouds-color), -0.312em -0.312em var(--back-clouds-color), 1.437em 0.375em var(--clouds-color), 0.5em -0.125em var(--back-clouds-color), 2.187em 0 var(--clouds-color), 1.25em -0.062em var(--back-clouds-color), 2.937em 0.312em var(--clouds-color), 2em -0.312em var(--back-clouds-color), 3.625em -0.062em var(--clouds-color), 2.625em 0em var(--back-clouds-color), 4.5em -0.312em var(--clouds-color), 3.375em -0.437em var(--back-clouds-color), 4.625em -1.75em 0 0.437em var(--clouds-color), 4em -0.625em var(--back-clouds-color), 4.125em -2.125em 0 0.437em var(--back-clouds-color);
          transition: 0.5s cubic-bezier(0, -0.02, 0.4, 1.25);
        }
        .theme-switch__stars-container {
          position: absolute; color: var(--stars-color); top: -100%; left: 0.312em; width: 2.75em; height: auto; transition: var(--transition);
        }
        .theme-switch__checkbox:checked + .theme-switch__container {
          background-color: var(--container-night-bg);
          background-image: linear-gradient(to bottom, var(--container-night-bg) 0%, #252a4a 100%);
        }
        .theme-switch__checkbox:checked + .theme-switch__container .theme-switch__circle-container {
          left: calc(100% - var(--circle-container-offset) - var(--circle-container-diameter));
        }
        .theme-switch__checkbox:checked + .theme-switch__container .theme-switch__moon {
          transform: translate(0);
        }
        .theme-switch__checkbox:checked + .theme-switch__container .theme-switch__clouds {
          bottom: -4.062em;
        }
        .theme-switch__checkbox:checked + .theme-switch__container .theme-switch__stars-container {
          top: 50%; transform: translateY(-50%);
        }

        /* ─── Light Mode Overrides ─── */
        body.light-mode .stApp { background: #f0f4f8 !important; }
        
        body.light-mode header[data-testid="stHeader"] {
            background: #f0f4f8 !important;
            color: #1e293b !important;
        }
        body.light-mode section[data-testid="stSidebar"] {
            background: #ffffff !important;
            color: #1e293b !important;
        }
        body.light-mode [data-testid="stSidebarNav"] {
            background: #ffffff !important;
        }
        body.light-mode [data-testid="stSidebarNav"] a,
        body.light-mode [data-testid="stSidebarNav"] span {
            color: #1e293b !important;
        }
        body.light-mode [data-testid="stSidebarUserContent"] {
            color: #1e293b !important;
        }
        
        body.light-mode .glass-card,
        body.light-mode .glass-panel {
            background: rgba(255, 255, 255, 0.8) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05) !important;
            color: #1e293b !important;
        }
        body.light-mode h1,
        body.light-mode h2,
        body.light-mode h3,
        body.light-mode h4,
        body.light-mode p,
        body.light-mode .stMarkdown,
        body.light-mode .app-header p {
            color: #1e293b !important;
        }
        body.light-mode .upload-zone {
            background: rgba(255, 255, 255, 0.5) !important;
            border: 2px dashed #94A3B8 !important;
        }
        body.light-mode .upload-text {
            color: #1e293b !important;
        }
        `;
        parentDoc.head.appendChild(style);
        
        // Find header and append toggle wrapper to avoid overlapping deploy button
        const header = parentDoc.querySelector('header[data-testid="stHeader"]');
        if (header) {
            header.style.position = 'relative';
            toggleWrapper.style.position = 'absolute';
            toggleWrapper.style.right = '12rem'; // Move further left from deploy button
            toggleWrapper.style.top = '50%';
            toggleWrapper.style.transform = 'translateY(-50%)';
            header.appendChild(toggleWrapper);
            
            // Inject "Explore" into header if empty
            if (!parentDoc.getElementById('header-explore-title')) {
                const title = parentDoc.createElement('div');
                title.id = 'header-explore-title';
                title.innerHTML = 'Explore';
                title.style.position = 'absolute';
                title.style.left = '6rem'; // Pushed far right to avoid the expanded custom nav button (which is ~12rem wide)
                title.style.top = '50%';
                title.style.transform = 'translateY(-50%)';
                title.style.fontSize = '1.2rem';
                title.style.fontWeight = '700';
                title.style.background = 'linear-gradient(135deg, #7C3AED, #10B981)';
                title.style.webkitBackgroundClip = 'text';
                title.style.webkitTextFillColor = 'transparent';
                header.appendChild(title);
            }
        } else {
            parentDoc.body.appendChild(toggleWrapper);
        }
        
        // Also rename "Pages" to "Explore" in the sidebar navigation
        const sidebarNav = parentDoc.querySelector('[data-testid="stSidebarNav"]');
        if (sidebarNav) {
            const pagesSpan = sidebarNav.querySelector('span');
            if (pagesSpan && pagesSpan.textContent.trim() === 'Pages') {
                pagesSpan.textContent = 'Explore';
            }
            
            // Rename "app home" to "🏠 Home"
            const linkSpans = sidebarNav.querySelectorAll('span');
            linkSpans.forEach(span => {
                if (span.textContent.trim() === 'app home') {
                    span.textContent = '🏠 Home';
                }
            });
        }
        
        // Event listener
        const checkbox = toggleWrapper.querySelector('.theme-switch__checkbox');
        
        // Restore previous state if needed
        if (parentDoc.body.classList.contains('light-mode')) {
            checkbox.checked = false;
        }
        
        checkbox.addEventListener('change', (e) => {
            if (!e.target.checked) {
                parentDoc.body.classList.add('light-mode');
            } else {
                parentDoc.body.classList.remove('light-mode');
            }
        });
    }
    </script>
    """, height=0, width=0)


import streamlit.components.v1 as components

def render_go_back_button():
    """
    Injects Javascript into the parent Streamlit DOM to replace the native
    'keyboard_double_arrow_left' sidebar collapse button with the user's custom Go Back button.
    """
    components.html("""
    <script>
    const parentDoc = window.parent.document;

    function injectCustomCss() {
        if (!parentDoc.getElementById('custom-go-back-css')) {
            const style = parentDoc.createElement('style');
            style.id = 'custom-go-back-css';
            style.innerHTML = `
            .custom-go-back-wrapper {
                background-color: white;
                text-align: center;
                width: 12rem;
                border-radius: 1rem;
                height: 3.5rem;
                position: relative;
                color: black;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                border: none;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                transition: all 0.3s ease;
                margin: 4px;
            }
            .custom-go-back-wrapper .icon-bg {
                background-color: #4ade80; 
                border-radius: 0.75rem;
                height: 3rem;
                width: 3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                position: absolute;
                left: 0.25rem;
                top: 0.25rem;
                z-index: 10;
                transition: width 0.5s;
            }
            .custom-go-back-wrapper:hover .icon-bg {
                width: calc(100% - 0.5rem); 
            }
            .custom-go-back-wrapper p {
                transform: translateX(1.5rem);
                margin: 0;
                z-index: 20;
                white-space: nowrap;
                pointer-events: none;
            }
            button[data-replaced="true"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                width: auto !important;
                height: auto !important;
            }
            /* Style for the expand button (collapsed state) */
            .custom-go-back-wrapper.expand-mode {
                width: 3.5rem;
                margin: 10px;
                border-radius: 50%;
                background-color: transparent;
            }
            .custom-go-back-wrapper.expand-mode .icon-bg {
                width: 3.5rem;
                height: 3.5rem;
                left: 0;
                top: 0;
                border-radius: 50%;
                transform: rotate(180deg);
                transition: transform 0.3s ease;
            }
            .custom-go-back-wrapper.expand-mode:hover .icon-bg {
                transform: rotate(180deg) scale(1.1);
                width: 3.5rem;
            }
            `;
            parentDoc.head.appendChild(style);
        }
    }

    function replaceSidebarButtons() {
        const spans = Array.from(parentDoc.querySelectorAll('span[data-testid="stIconMaterial"]'));
        
        // 1. Replace the Collapse (Left) Button
        const leftSpan = spans.find(s => s.textContent.trim() === 'keyboard_double_arrow_left');
        if (leftSpan) {
            const btn = leftSpan.closest('button');
            if (btn && !btn.hasAttribute('data-replaced')) {
                btn.setAttribute('data-replaced', 'true');
                btn.innerHTML = '';
                injectCustomCss();
                btn.innerHTML = `
                <div class="custom-go-back-wrapper">
                    <div class="icon-bg">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" height="25px" width="25px">
                        <path d="M224 480h640a32 32 0 1 1 0 64H224a32 32 0 0 1 0-64z" fill="#000000"></path>
                        <path d="m237.248 512 265.408 265.344a32 32 0 0 1-45.312 45.312l-288-288a32 32 0 0 1 0-45.312l288-288a32 32 0 1 1 45.312 45.312L237.248 512z" fill="#000000"></path>
                      </svg>
                    </div>
                    <p>Close</p>
                </div>
                `;
            }
        }

        // 2. Replace the Expand (Right) Button
        const rightSpan = spans.find(s => s.textContent.trim() === 'keyboard_double_arrow_right');
        if (rightSpan) {
            const btn = rightSpan.closest('button');
            if (btn && !btn.hasAttribute('data-replaced')) {
                btn.setAttribute('data-replaced', 'true');
                btn.innerHTML = '';
                injectCustomCss();
                btn.innerHTML = `
                <div class="custom-go-back-wrapper expand-mode">
                    <div class="icon-bg">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" height="25px" width="25px">
                        <path d="M224 480h640a32 32 0 1 1 0 64H224a32 32 0 0 1 0-64z" fill="#000000"></path>
                        <path d="m237.248 512 265.408 265.344a32 32 0 0 1-45.312 45.312l-288-288a32 32 0 0 1 0-45.312l288-288a32 32 0 1 1 45.312 45.312L237.248 512z" fill="#000000"></path>
                      </svg>
                    </div>
                </div>
                `;
            }
        }
    }

    // Run once immediately
    replaceSidebarButtons();

    // Use a MutationObserver to continuously watch for DOM changes,
    // so if Streamlit mounts the expand/collapse button later, we catch it!
    const observer = new MutationObserver((mutations) => {
        replaceSidebarButtons();
    });
    observer.observe(parentDoc.body, { childList: true, subtree: true });

    </script>
    """, height=0, width=0)
