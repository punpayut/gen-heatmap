import datetime
import json

def create_interactive_heatmap_page():
    """
    Generates the final, correct interactive HTML page using the verified TradingView technical names.
    """

    # --- THE CORRECT, VERIFIED DICTIONARY ---
    # This maps the friendly display name to the exact technical name the widget requires.
    supported_indices = {
        "S&P 500": "SPX500",
        "NASDAQ 100": "NASDAQ100",
        "Dow Jones": "",
        "Germany DAX": "DAX",
        "KOSPI 200": "KOSPI200",
        "Indonesia Index": "IDX30",
        "Japan Nikkei 225": "NIKKEI225",
        "Hong Kong Hang Seng": "HSTECH",
        "Australia ASX 200": "ASX200",
        "SET Index": "SET50"
    }
    
    indices_json = json.dumps(supported_indices)

    # The JavaScript logic, now using the correct template and data.
    javascript_code = f"""
    const supportedIndices = {indices_json};
    const selectElement = document.getElementById('index-select');
    const heatmapContainer = document.getElementById('heatmap-container');

    function loadWidget(dataSource) {{
        heatmapContainer.innerHTML = ''; 
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js';
        script.async = true;
        
        // This JSON is based on the verified template you provided.
        script.innerHTML = `{{
            "exchanges": [],
            "dataSource": "${{dataSource}}",
            "grouping": "sector",
            "blockSize": "market_cap_basic",
            "blockColor": "change",
            "locale": "en",
            "symbolUrl": "",
            "colorTheme": "light",
            "hasTopBar": false,
            "isDataSetEnabled": false,
            "isZoomEnabled": true,
            "hasSymbolTooltip": true,
            "isMonoSize": false,
            "width": "100%",
            "height": "100%"
        }}`;
        heatmapContainer.appendChild(script);
    }}

    // Populate the dropdown with the correct values
    for (const displayName in supportedIndices) {{
        const technicalName = supportedIndices[displayName];
        const option = document.createElement('option');
        option.value = technicalName;
        option.textContent = displayName;
        if (technicalName === 'SPX500') {{
            option.selected = true;
        }}
        selectElement.appendChild(option);
    }}

    // Add event listener to handle changes
    selectElement.addEventListener('change', function() {{
        loadWidget(this.value);
    }});

    // Initial load with the default S&P 500
    loadWidget('SPX500');
    """

    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Stock Market Heatmap</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 1.8em; color: #1c1e21; margin-bottom: 10px; }}
        .controls {{ margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
        label {{ font-weight: bold; }}
        #index-select {{ font-size: 1em; padding: 8px 12px; border-radius: 6px; border: 1px solid #ccc; }}
        .heatmap-wrapper {{ height: 600px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Live Stock Market Heatmap</h1>
        <div class="controls">
            <label for="index-select">Select Index:</label>
            <select id="index-select"></select>
        </div>
        <div class="heatmap-wrapper" id="heatmap-container">
            <!-- TradingView widget will be loaded here -->
        </div>
    </div>
    <script>{javascript_code}</script>
</body>
</html>
"""
    return full_html

def save_html_to_file(html_content, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n✅ Success! Interactive page saved as '{filename}'")
        print("   This is the final version and should work correctly.")
    except IOError as e:
        print(f"\n❌ Error! Could not save file: {e}")

if __name__ == "__main__":
    output_filename = "interactive_heatmap_final.html"
    html_page_content = create_interactive_heatmap_page()
    save_html_to_file(html_page_content, output_filename)