awk '{
  #gsub(/[,_;:()+[\]\x2E-]/, " ", $0);
  
  $2 = tolower($2);
  sum[$2]=0;
  for (i=3; i<=NF; i++){
  	sum[$2] = sum[$2] + $i;				#sumar los atributos largo, ancho
  	#print $i;
  }
  
  sum[$2]=sum[$2]/(NF-2);				#tomar el promedio parcial de los datos
  
  media[$2]=media[$2]+sum[$2];			#sumatoria de los promedios parciales
  Total[$2]++;							#total por tipo de hoja
}

END {
  for (x in media) {
    #split(x, a, SUBSEP);
    print x, media[x]/Total[x];
  }
} ' $*