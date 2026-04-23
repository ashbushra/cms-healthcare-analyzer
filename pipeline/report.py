import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from analyze import get_top_procedures, get_city_variance, get_charge_ratio

def generate_report():
    print("Generating HTML report...")
    
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    
    top_procedures = get_top_procedures()
    city_variance = get_city_variance()
    charge_ratio = get_charge_ratio()
    
    html_out = template.render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        top_procedures=top_procedures,
        city_variance=city_variance,
        charge_ratio=charge_ratio
    )
    
    os.makedirs('outputs', exist_ok=True)
    
    output_path = os.path.join('outputs', 'report.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
        
    print(f"Report successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_report()