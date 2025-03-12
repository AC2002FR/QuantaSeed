# QuantaSeed 🌱🔬 - True Quantum Entropy Generator

QuantaSeed is a **cross-platform command-line tool** that generates **true quantum entropy** using the **ANU QRNG API** from the Australian National University.  
It ensures **high-quality randomness** for cryptographic security, password generation, and any security-sensitive application. 

## 🚀 Features
- ✅ **True quantum entropy** from a real quantum random number generator (ANU QRNG)
- ✅ **Cross-platform** (Windows, Linux, macOS)
- ✅ **Secure & cryptographically strong**
- ✅ **Customizable length** (`--length` option)
- ✅ **Execution cooldown (90 seconds for --length to prevent excessive API calls)**
- ✅ **Easy to run and store on GitHub**

## 🔬 Source of Entropy
QuantaSeed retrieves quantum-generated random numbers from the **Australian National University's Quantum Random Number Generator (ANU QRNG)**. This system extracts randomness from vacuum fluctuations, ensuring **true quantum entropy** for high-security applications.

More information: [ANU QRNG API Documentation](https://qrng.anu.edu.au/contact/api-documentation/)

## 🔧 Installation & Usage
### 📥 Clone the repository
```sh
git clone https://github.com/AC2002FR/QuantaSeed.git
cd QuantaSeed
```

### 📦 Install Dependencies
Before running QuantaSeed, make sure you have the required dependencies:
```sh
pip install -r requirements.txt
```

## 🚀 Run the script
### Linux/MacOS :
```sh
chmod +x quantaseed.py
./quantaseed.py --length 50
```
### Windows : 
```sh
python quantaseed.py --length 50
```

## 🛠 Example Output : 
```sh
🔄 Attempting ANU QRNG (length=50)...
🔑 Generated Entropy: vNz8Yg3KdAq+LpZbT1xJRm5HWUeoF2Xs
```

## ⚙️ Command-line Options
| Option | Description |
|--------|-------------|
| `-l, --length <number>` | Specify string length (default: 32). **(90s cooldown enforced)** |
| `-s, --silent` | Silent mode (outputs only the entropy string) |
| `-c, --copy` | Copies the generated entropy string to clipboard |
| `-a, --show-api` | Displays the API source used and exits |
| `-h, --help` | Shows help in English |
| `--aide` | Shows help in French |

## 🛡️ Why QuantaSeed ? 
Unlike pseudo-random number generators (PRNGs), **QuantaSeed directly sources randomness from quantum physics**, ensuring high entropy for cryptographic applications. Using quantum fluctuations from vacuum energy, it provides entropy that is **unpredictable, unbiased, and secure**.

## 🏗️ Contributing
Want to improve the project? Feel free to fork and submit pull requests! 🚀

## 📜 License
MIT License - Free to use, modify, and distribute.
