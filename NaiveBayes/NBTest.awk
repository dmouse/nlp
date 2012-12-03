awk '
FILENAME==model{
  modelo[$1,$2]=$3;
  classes[$1]=1;
  next;
}
BEGIN {
  EPSILON = 0.00001;
  print "--------------------------------------------------------";

  print "--------------------------------------------------------";
}
{
  maximo = 0;
  clase = "NINGUNA";

  for (x in classes) {
    probabilidad=0;
    for (i=2; i<=NF; i++) {
      if ((x,$i) in modelo) probabilidad = probabilidad + log(modelo[x,$i]+1);
      else probabilidad = probabilidad + log(EPSILON+1);
    }
    if (probabilidad > maximo) {
      maximo = probabilidad;
      clase = x;
    }
  }

  print $1, clase, maximo, " : ", $2, $3, $4, $5"...";
}

END{
  print "--------------------------------------------------------";

  print "--------------------------------------------------------";
}' model=$1 $* 
