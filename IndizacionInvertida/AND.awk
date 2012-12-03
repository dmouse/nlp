awk '
FILENAME==indice{
  df[$1]=$3;
  posting[$1]=$6;
  next;
}

FILENAME==chistes{
  chiste[++cont]=$0;
  next;
}


function AND_NOT(p1, p2) {
  answer = "";
  
  na = split(p1, a, ",");
  nb = split(p2, b, ",");

  pp1 = 1;
  pp2 = 1;

  while ((pp1 <= na) && (pp2 <= nb)) {
    if (a[pp1] == b[pp2]) {
      pp1++;
      pp2++;
    } else {
      if (a[pp1] < b[pp2]) {
        answer = answer "," a[pp1];
        pp1++;
      } else pp2++;
    }
  }

  return substr(answer, 2);
}

function AND(p1, p2) {
  answer = "";

  na = split(p1, a, ",");
  nb = split(p2, b, ",");

  pp1 = 1;
  pp2 = 1;

  while ((pp1 <= na) && (pp2 <= nb)) {
    if (a[pp1] == b[pp2]) {
      answer = answer "," a[pp1];
      pp1++;
      pp2++;
    } else {
      if (a[pp1] < b[pp2]) pp1++;
      else pp2++;
    }
  }

  return substr(answer,2);
}

function OR(p1, p2) {
  answer = "";

  na = split(p1, a, ",");
  nb = split(p2, b, ",");

  pp1 = 1;
  pp2 = 1;

  while ((pp1 <= na) || (pp2 <= nb)) {
    if (pp1 > na) {
      answer = answer "," b[pp2]; 
      pp2++;
    } else {
      if (pp2 > nb) {
        answer = answer "," a[pp1]; 
        pp1++;
      } else {

        if (a[pp1] == b[pp2]) {
          answer = answer "," a[pp1];
          pp1++;
          pp2++;
        } else {
          if (a[pp1] < b[pp2]) {
            answer = answer "," a[pp1];
            pp1++;
          } else {
            answer = answer "," b[pp2];
            pp2++;
          }
        }


      }
    }
  }

  return substr(answer,2);
}

{
  if (NF == 1) {
    ne = split(posting[$1], a, ",");
    for (i=1; i<=ne; i++) {
      print chiste[a[i]];
      print "";
    }
  } else {
    lista = posting[$1];
    for (i=2; i<=NF; i++) {
      lista=AND(lista, posting[$i]);
    }
    ne = split(lista, a, ",");
    print "------------------------------------";
    print "Se encontraron ", ne, " resultados."
    print "------------------------------------";
    for (i=1; i<=ne; i++) {
      print i " : " substr(chiste[a[i]], index(chiste[a[i]], " ")+1) "\n";
    }
  }
}' indice=$1 chistes=$2 $*
