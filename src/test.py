import subprocess
import re

# Run command and capture output
result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
output = result.stdout.strip()  # Avoid using repr()

# Debug: Print the raw output to inspect formatting
print(output)

pattern = re.compile(r"\|\s*([\d,\s]+)\s*>\s*:\s*([+-]?\d+\.\d+(?:e[+-]?\d+)?)\s*([+-]\s*\d+\.\d+(?:e[+-]?\d+)?)\s*j")

matches = pattern.findall(output)

