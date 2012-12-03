{
#  ++doc;                                 				#documento actual
  for (i=2; i<=NF; i++) {                				#para todas las palaras del documento    
       doc = $1;
       $i = tolower($i);
       gsub(/-_\//," ",$i);
       gsub(/\W|[0-9_]/,"",$i);

#      gsub(/[^a-zA-Z0-9áéúíóüÜ]/," ",$i);
#      gsub]


	if($i != ""){
       indice[$i] = indice[$i] "," doc; 				#indice[]=indice documento
       frecdoc[$i,doc]++;                				#frecuencia de la palabra por doc
       pos[$i,doc]=pos[$i,doc] "," i ;  				#posicion palabra por documentoo
       df[$i]++;			 			 				#incrementa la total frecuencia de la palabra
    }
  }
  #delete vocabulario;
  #delete frecdoc;
}
END{
    for(x in indice){
    	aux=0;
	d = substr(indice[x], 2);
	ln = split(d, a, ",");
	print x "," df[x] ":";
	for(j = 1; j <= ln; j++){
		p = substr(pos[x,a[j]], 2);
		if(aux != a[j]){
			print   a[j] "," frecdoc[x,a[j]] "," p;
       }
       aux=a[j];
       }
       print "";
    }
    
}	 
