awk '{
  gsub(/[,_;:()+[\]\x2E-]/, " ", $0);
  for (i=3; i<=NF; i++) frecuencia[tolower($2),tolower($i)]++;
  Total[tolower($2)] = Total[tolower($2)] + (NF - 2);
}
END {
  for (x in frecuencia) {
    split(x, a, SUBSEP);
    print a[1], a[2], frecuencia[x]/Total[a[1]];
  }
} ' $*
