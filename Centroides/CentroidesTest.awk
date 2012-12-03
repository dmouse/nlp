awk '
FILENAME==model{
  modelo[$1] = $2;
  clases[$1] = 2;
  next;
}
function abs(x){
	return (((x < 0.0) ? -x : x) + 0.0)
}

BEGIN {
  EPSILON = 0.00001;
}
{
  dif=0;
  minimo = 999999999999999999999999999;
  for (x in clases) {
    sum=0;
    for (i=2; i<=NF; i++) {
    	sum=sum + $i;
    }
    
    sum = sum/(NF-1);
    
    dif = abs(modelo[x]-sum);
    
    if ( dif < minimo) {
      minimo = dif;
      clase = x;
    }
  }
  print "--------------------------------------------------------";
  print $1, clase, minimo, " : ", $2, $3, $4, $5"...";
  print "--------------------------------------------------------";
}

END{
	
}' model=$1 $* 
