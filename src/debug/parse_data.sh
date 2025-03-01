#!/bin/bash
echo "Superpositioned (state) test has been sent to data.txt"
grep -n -Ee "\b1\s+1\s+0\s+0\b" -e "\b1\s+0\s+1\s+0\b" -e "\b0\s+1\s+0\s+1" -e "\b0\s+0\s+1\s+1\b" parsed.txt > data.txt

echo "0 (state) test has been sent to data0.txt"
grep -n -Ee "\b1\s+1\s+0\s+0\b" -e "\b1\s+0\s+1\s+0\b" -e "\b0\s+1\s+0\s+1" -e "\b0\s+0\s+1\s+1\b" parsed0.txt > data0.txt