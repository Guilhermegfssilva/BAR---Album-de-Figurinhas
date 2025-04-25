# BAR 

Protótipo inicial do album de figurinhas


Estrutura:

Pasta /Images: todas as imagens que desejar serem incluídas no album, devem estar dentro desta pasta no formato JPEG para
que seja possível gerar o arquivo de encode.

O arquivo de encode é o principal utilizado para o reconhecimento da imagem.

Depois de instalar todas as dependencias e inserir as imagens no diretório, é necessário rodar o EncodeGenerator.py, com isso,
será gerado o arquivo que armazena o mapeamento de cada imagem.

Após isso, pode-se executar o main.py para colocar o servidor para rodar....


Dentro da pasta 'templates' tem um HTML básico com um input de imagem para acionar o reconhecimento, para seu funcionamento o main precisa estar rodando
e o arquivo de encode precisa estar gerado.

