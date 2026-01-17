# Create the file
cat > install.sh << 'END'
#!/bin/bash
echo "Installing SQLiAutoPwn..."
echo "=========================="

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.7+"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "🔍 Checking for SQLMap..."
if ! command -v sqlmap &> /dev/null; then
    echo "⚠️  SQLMap not found!"
    echo "📥 Installing SQLMap..."
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
    echo "✅ SQLMap installed in ./sqlmap/"
    echo ""
    echo "To use SQLMap: python3 sqlmap/sqlmap.py"
fi

chmod +x sqli_autopwn.py

echo ""
echo "✅ Installation complete!"
echo "🚀 Usage: python3 sqli_autopwn.py http://target.com"
END

# Make it executable
chmod +x install.sh
