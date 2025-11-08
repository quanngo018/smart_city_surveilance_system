"""
Early CSS Injection Component
Injects CSS into page HEAD to prevent black flash on page transitions.
"""

import streamlit as st
import streamlit.components.v1 as components


def inject_head_css(css_content: str) -> None:
    """
    Inject CSS into the HTML HEAD section.
    This loads before body content, preventing black flash.
    
    Args:
        css_content: CSS content to inject (without <style> tags)
    """
    
    # Create HTML with inline CSS that injects into head
    head_inject_html = f"""
    <script>
        // Inject CSS into HEAD as early as possible
        (function() {{
            // Check if style already exists
            if (!document.getElementById('early-white-theme')) {{
                var style = document.createElement('style');
                style.id = 'early-white-theme';
                style.innerHTML = `{css_content}`;
                
                // Insert at the beginning of head for highest priority
                var head = document.head || document.getElementsByTagName('head')[0];
                head.insertBefore(style, head.firstChild);
                
                // Also set body background immediately
                document.body.style.backgroundColor = '#FFFFFF';
                document.documentElement.style.backgroundColor = '#FFFFFF';
            }}
        }})();
    </script>
    """
    
    # Inject using components
    components.html(head_inject_html, height=0, width=0)


def apply_anti_flash_css() -> None:
    """
    Apply aggressive anti-flash CSS that loads immediately.
    Call this at the very top of every page.
    """
    
    critical_css = """
        html, body {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        * {
            transition: none !important;
            animation-duration: 0s !important;
        }
        
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        .main,
        .block-container,
        header[data-testid="stHeader"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        [data-testid="stDecoration"] {
            display: none !important;
            background-color: #FFFFFF !important;
        }
        
        [data-testid="stToolbar"],
        [data-testid="stStatusWidget"] {
            background-color: #FFFFFF !important;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #F5F5F5 !important;
        }
        
        footer, #MainMenu {
            visibility: hidden;
        }
    """
    
    inject_head_css(critical_css)


# Minimal inline CSS for immediate application
IMMEDIATE_WHITE_CSS = """
<style>
    html { background: #FFF !important; }
    body { background: #FFF !important; margin: 0; padding: 0; }
    * { transition: none !important; }
    [data-testid="stApp"] { background: #FFF !important; }
    [data-testid="stDecoration"] { display: none !important; }
</style>
"""
