awk '{
  ++contador;
  for (i=2; i<=NF; i++) {
    if (!($i in vocabulario)) {
      indice[$i] = indice[$i] "," contador;
      vocabulario[$i]=1;
      df[$i]++;
    }
  }
  delete vocabulario;
}
END {
  for (x in indice) print x " [ " df[x] " ] : " substr(indice[x], 2);
}' $*
