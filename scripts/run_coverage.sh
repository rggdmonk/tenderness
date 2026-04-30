#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# 1️⃣ Clean previous run
# -----------------------------
echo "Erasing previous coverage data..."
coverage erase
rm -rf htmlcov_total

# -----------------------------
# 2️⃣ Run all test suites
# -----------------------------
echo "Running unit tests..."
coverage run --data-file=.coverage.unit -m pytest tests -m "not eternal_contract and not e2e"

echo "Running eternal contract tests..."
coverage run --data-file=.coverage.eternal_contract -m pytest tests -m "eternal_contract"

echo "Running e2e tests..."
coverage run --data-file=.coverage.e2e -m pytest tests -m "e2e"

# -----------------------------
# 3️⃣ Combine and report
# -----------------------------
echo "Combining all coverage data..."
coverage combine .coverage.unit .coverage.eternal_contract .coverage.e2e

echo "Generating combined coverage report..."
coverage report
coverage html -d htmlcov_total

echo "✅ All done!"
echo " - Combined HTML: htmlcov_total/index.html"