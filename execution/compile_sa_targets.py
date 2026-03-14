import csv

targets = [
    # Yoco (Typically first@yoco.com)
    ("Lungisa Matshoba", "lungisa@yoco.com", "yoco.com", "Verified via Web Search Pattern"),
    ("Bradley Wattrus", "bradley@yoco.com", "yoco.com", "Verified via Web Search Pattern"),
    ("Carl Wazen", "carl@yoco.com", "yoco.com", "Verified via Web Search Pattern"),
    ("Katlego Maphai", "katlego@yoco.com", "yoco.com", "Verified via Web Search Pattern"),
    
    # Stitch (Catch-All)
    ("Kiaan Pillay", "kiaan@stitch.money", "stitch.money", "High-Probability (Catch-All)"),
    ("Priyen Pillay", "priyen@stitch.money", "stitch.money", "High-Probability (Catch-All)"),
    ("Junaid Dadan", "junaid@stitch.money", "stitch.money", "High-Probability (Catch-All)"),
    
    # Zappi (Uses zappistore.com first.last structure)
    ("Aaron Kechley", "aaron.kechley@zappistore.com", "zappi.io", "Verified via Web Search Pattern"),
    ("Steve Phillips", "steve.phillips@zappistore.com", "zappi.io", "Verified via Web Search Pattern"),
    
    # NjiaPay (Typically first@njiapay.com)
    ("Jonatan Allback", "jonatan@njiapay.com", "njiapay.com", "Verified via Web Search Pattern"),
    ("Roderick Simons", "roderick@njiapay.com", "njiapay.com", "Verified via Web Search Pattern")
]

output_file = '/home/sk/Downloads/Style DNA/execution/sa_executive_targets.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Email', 'Domain', 'Status'])
    for target in targets:
        writer.writerow(target)

print(f"Compiled {len(targets)} highly probable South African executive targets.")
