import streamlit.components.v1 as components
import streamlit as st

def inject_custom_sidebar_collapse():
    """
    Injects Javascript into the parent Streamlit DOM to replace the native
    'keyboard_double_arrow_left' sidebar collapse button with the user's custom Go Back button.
    """
    components.html("""
    <script>
    // Run after a short delay to ensure Streamlit's React tree is fully rendered
    setTimeout(() => {
        const parentDoc = window.parent.document;
        
        // Find the specific span containing 'keyboard_double_arrow_left'
        const spans = Array.from(parentDoc.querySelectorAll('span[data-testid="stIconMaterial"]'));
        const arrowSpan = spans.find(s => s.textContent.trim() === 'keyboard_double_arrow_left');
        
        if (arrowSpan) {
            // The button is usually the closest button ancestor
            const nativeBtn = arrowSpan.closest('button');
            
            if (nativeBtn && !nativeBtn.hasAttribute('data-replaced')) {
                nativeBtn.setAttribute('data-replaced', 'true');
                
                // Hide the native icon content
                nativeBtn.innerHTML = '';
                
                // Inject the user's custom CSS into the parent document
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
                    }
                    /* Ensure Streamlit's default button styles don't conflict */
                    button[data-replaced="true"] {
                        background: transparent !important;
                        border: none !important;
                        padding: 0 !important;
                        width: auto !important;
                        height: auto !important;
                    }
                    `;
                    parentDoc.head.appendChild(style);
                }
                
                // Set the custom HTML
                nativeBtn.innerHTML = `
                <div class="custom-go-back-wrapper">
                    <div class="icon-bg">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" height="25px" width="25px">
                        <path d="M224 480h640a32 32 0 1 1 0 64H224a32 32 0 0 1 0-64z" fill="#000000"></path>
                        <path d="m237.248 512 265.408 265.344a32 32 0 0 1-45.312 45.312l-288-288a32 32 0 0 1 0-45.312l288-288a32 32 0 1 1 45.312 45.312L237.248 512z" fill="#000000"></path>
                      </svg>
                    </div>
                    <p>Go Back</p>
                </div>
                `;
            }
        }
        
        // Also handle the expand button if they collapse it! (keyboard_double_arrow_right)
        // Actually, we can style BOTH if we want, or just leave the expand button as default.
        // Let's replace the expand button too if it appears.
        const rightArrowSpan = spans.find(s => s.textContent.trim() === 'keyboard_double_arrow_right');
        if (rightArrowSpan) {
             const expandBtn = rightArrowSpan.closest('button');
             if (expandBtn && !expandBtn.hasAttribute('data-replaced')) {
                 expandBtn.setAttribute('data-replaced', 'true');
                 expandBtn.innerHTML = `
                    <div class="custom-go-back-wrapper" style="width: 3.5rem;">
                        <div class="icon-bg" style="width: 3rem; transform: rotate(180deg);">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" height="25px" width="25px">
                            <path d="M224 480h640a32 32 0 1 1 0 64H224a32 32 0 0 1 0-64z" fill="#000000"></path>
                            <path d="m237.248 512 265.408 265.344a32 32 0 0 1-45.312 45.312l-288-288a32 32 0 0 1 0-45.312l288-288a32 32 0 1 1 45.312 45.312L237.248 512z" fill="#000000"></path>
                          </svg>
                        </div>
                    </div>
                 `;
             }
        }
    }, 500);
    </script>
    """, height=0, width=0)
