{
  #++doc;                                 			#documento actual
  for (i=2; i<=NF; i++) {                				#para todas las palaras del documento
       doc = $1
       indice[$i] = indice[$i] "," doc; 				#indice[]=indice documento
       frecdoc[$i,doc]++;                				#frecuencia de la palabra por doc
       pos[$i,doc] = pos[$i,doc] ", " i ;  				#posicion palabra por documentoo
       df[$i]++;			 			 	#incrementa la total frecuencia de la palabra
  }
}
END{
  
  for(x in indice){
    aux=0;
	    d = substr(indice[x], 2);
	ln = split(d, a, ",");
	print x "," df[x] ":";
#	print x "," df[x] ":";
	for(j = 1; j <= ln; j++){
		p = substr(pos[x,a[j]], 2);
		if(aux != a[j]){
#			print  "\t" a[j] "," frecdoc[x,a[j]] ": <" p " >;";
			print  "\t" a[j] "," frecdoc[x,a[j]] " " p " ";
       }
       aux=a[j];
       }
       print "";
    }
    
}	 
