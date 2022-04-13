#!/bin/bash

cd /tmp

diretorioArqs="$1"
tipoArquivoDir="$2"
tipoArquivoUltimos="$3"
prefixoLinks="$4"
numeroLinksSimbolicos="$5"
apagaDadosComMaisQueTantosDias="$6"

#echo $diretorioArqs
#echo $tipoArquivoDir
#echo $tipoArquivoUltimos
#echo $prefixoLinks
#echo $numeroLinksSimbolicos
#echo $apagaDadosComMaisQueTantosDias 

#echo "Atualiza Links Simbólicos"
cd ${diretorioArqs}
rm -rf ${prefixoLinks}_*.${tipoArquivoUltimos}
arqs=( $(find . -iname '*.'${tipoArquivoDir} | sort -r ) )
quantidadeArquivosNoDir=${#arqs[@]}

i=${numeroLinksSimbolicos}
# #Compara número de arquivos, com o número de links que desejam ser gerados
# if [ quantidadeArquivosNoDir > numeroLinksSimbolicos  ]; then
#     i=${quantidadeArquivosNoDir}
# fi


while [ $i -gt 0 ]; do
        let j=${numeroLinksSimbolicos}-i
        #data=$(echo $data | cut -c 11-12)
        arqAtual=${arqs[$j]}
        arr=(${arqAtual//./ })
        arr1=(${arr//_/ })
        #echo ${arr1[2]}
        let indiceArq=${numeroLinksSimbolicos}-i+1
        ln -fs ${arqs[$j]} ${diretorioArqs}/${prefixoLinks}_$indiceArq.${tipoArquivoUltimos}
        let i-=1
done

#Apaga dados com mais de "apagaDadosComMaisQueTantosDias" dia
find . -iname '*.'${tipoArquivoDir} -mtime +${apagaDadosComMaisQueTantosDias} | xargs rm -f

