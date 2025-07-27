#!/bin/bash
# Script to install Microsoft ODBC Driver 18 for SQL Server on macOS

echo "Updating Homebrew..."
brew update

echo "Installing unixODBC..."
brew install unixodbc

echo "Installing Microsoft ODBC Driver 18 for SQL Server..."
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_NO_AUTO_UPDATE=1 brew install msodbcsql18

echo "Installation complete. Please verify the driver installation with:"
echo "odbcinst -q -d -n 'ODBC Driver 18 for SQL Server'"
