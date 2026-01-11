#!/usr/bin/env bash
set -euo pipefail

clear

# --- ANSI Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- Setup ---
TARGET="broken.py"
SOURCE="files/broken.py"

if [[ -f "$TARGET" ]]; then
  rm "$TARGET"
fi

if [[ ! -f "$SOURCE" ]]; then
  echo -e "${RED}ERROR: $SOURCE not found!${NC}"
  exit 1
fi

# --- AUTOMATED SETUP ---
# Hardcoded values as requested
INITIAL_CASH=2000000
SALARY=1250

CASH=$INITIAL_CASH
TICK=1

# Overwrite target safely instead of rm (preserves editor swap files)
cp -f "$SOURCE" "$TARGET"

echo "================================="
echo -e "${YELLOW}VIM Startup! Fix the code before you go broke.${NC}"
echo "CASH: £$CASH | SALARY: £$SALARY"
echo "================================="

STATUS="broken"
START_TIME=$(date +%s)

# --- Game Loop ---
while true; do

  if ((CASH < (INITIAL_CASH / 4))); then
    COLOR=$RED
  else
    COLOR=$GREEN
  fi

  # Update UI
  printf "\rSTATUS: %-7s | CASH: ${COLOR}£%6d${NC} " "$STATUS" "$CASH"

  if python3 "$TARGET" >/dev/null 2>&1; then
    STATUS="fixed"
    printf "\rSTATUS: %-7s | CASH: ${GREEN}£%6d${NC} " "$STATUS" "$CASH"
    break
  fi

  # Subtract salary AFTER the check to give the player a fair final second
  CASH=$((CASH - SALARY))
  SALARY=$((SALARY + 10))

  # Check lose condition
  if ((CASH <= 0)); then
    STATUS="lost"
    printf "\rSTATUS: %-7s | CASH: ${RED}£%6d${NC} " "$STATUS" 0
    break
  fi

  sleep "$TICK"
done

echo -e "\n================================="

if [[ "$STATUS" == "fixed" ]]; then
  ELAPSED=$(($(date +%s) - START_TIME))
  echo -e "🎉 ${GREEN}WIN${NC} — fixed in ${ELAPSED}s | CASH remaining: £$CASH"
else
  echo -e "💸 ${RED}You went bankrupt! [GAME OVER]${NC}"
fi

echo "================================="
