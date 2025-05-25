from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import io
import csv

app = Flask(__name__)

# Fixed list of capacitor category URLs
CAPACITOR_URLS = [
    "https://nepp.nasa.gov/npsl/Capacitors/Cap_type.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/Cer_type.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/gla_type.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/Tan_type.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/pla_type.htm",
    
    #Ceramic CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/20/20.htm",
    # MIL-PRF-20, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/123/123.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/39014.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/55681.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/49467.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/49470.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR05.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR06.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR07.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR08.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR75.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR76.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR77.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR78.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/20/CCR79.htm",
    # MIL-PRF-123, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS05.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS06.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS07.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS11.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS12.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS14.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS15.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS16.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS51.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS52.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS53.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS54.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS22.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS23.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS24.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS55.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS56.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/123/CKS57.htm",
    # MIL-PRF-39014, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR05.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR06.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR11.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR12.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR14.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR15.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR22.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR23.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39014/CKR24.htm",
    #MIL-PRF-55681, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR01.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR03.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR04.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR05.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR06.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR11.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR12.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR13.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR14.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR31.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR32.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR33.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR34.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55681/CDR35.htm",
    # MIL-PRF-49467, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv01.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv02.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv03.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv04.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv05.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49467/hv07.htm",
    # MIL-PRF-49470
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps01_050v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps01_100v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps01_200v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps01_500v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps02_050v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps02_100v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps02_200v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/49470/ps02_500v.htm",
    #DSCC-DWG-87106, CAPACITORS 
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106_50v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106_100v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106_200v.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87106/87106_500v.htm",
    
    # Glass Capacitors
    "https://nepp.nasa.gov/npsl/Capacitors/23269/23269.htm",
    # MIL-PRF-23269, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/23269/CYR10.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/23269/CYR15.htm",
    
    # Plastic Film Capacitors
    "https://nepp.nasa.gov/npsl/Capacitors/83421/83421.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87217/87217.htm",
    # MIL-PRF-83421, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/83421/CRH01.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/83421/CRH02.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/83421/CRH03.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/83421/CRH04.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/83421/CRH05.htm",
    # MIL-PRF-87217, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/87217/CHS01.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87217/CHS02.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/87217/CHS03.htm",
    
    # Tantalum Capacitors
    "https://nepp.nasa.gov/npsl/Capacitors/39003/39003.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39006/39006.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55365/55365.htm",
    # MIL-PRF-39003, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSR13.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSR09.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSR33.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSR21.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSS13.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39003/CSS33.htm",
    # MIL-PRF-39006, CAPACITORS    
    "https://nepp.nasa.gov/npsl/Capacitors/39006/CLR79.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39006/CLR81.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39006/CLR90.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/39006/CLR91.htm",
    # MIL-PRF-55365, CAPACITORS
    "https://nepp.nasa.gov/npsl/Capacitors/55365/CWR06.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55365/CWR09.htm",
    "https://nepp.nasa.gov/npsl/Capacitors/55365/CWR11.htm",
    
        
       
        
    
    
]

# In-memory cache
cache = {}

def search_part_number(part_number):
    """Search the part number in the fixed list of capacitor pages."""
    if part_number in cache:
        return cache[part_number]

    results = []

    for url in CAPACITOR_URLS:
        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")
            tables = soup.find_all("table")

            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if not cells:
                        continue
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if any(part_number.lower() in cell.lower() for cell in row_data):
                        results.append((url, row_data))
        except Exception as e:
            print(f"Error accessing {url}: {e}")

    cache[part_number] = results
    return results

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    part_number = ""
    if request.method == "POST":
        part_number = request.form["part_number"]
        results = search_part_number(part_number)
    return render_template("index.html", results=results, part_number=part_number)

@app.route("/download", methods=["POST"])
def download():
    part_number = request.form["part_number"]
    results = search_part_number(part_number)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Page URL", "Matched Row"])
    for url, row in results:
        writer.writerow([url, ", ".join(row)])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{part_number}_results.csv"
    )

if __name__ == "__main__":
    app.run(debug=True)
