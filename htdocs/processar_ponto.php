<?php
// Verifica se o botão "Bater ponto" foi pressionado
if(isset($_POST['bater_ponto'])) {
    // Envia uma requisição para o servidor Flask
    $url = 'http://localhost:5000/reconhecimento_facial';
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    curl_close($ch);

    // Processa a resposta do servidor Flask
    $responseData = json_decode($response, true);
    
    // Verifica se o reconhecimento facial foi bem-sucedido
    if(isset($responseData['mensagem']) && $responseData['mensagem'] == 'Rosto reconhecido') {
        // Decodifica a imagem base64
        $img_base64 = $responseData['imagem_base64'];
        $img_data = base64_decode($img_base64);
        
        // Salva a imagem em um arquivo
        $img_path = 'imagem_reconhecida.jpg';
        file_put_contents($img_path, $img_data);
        
        // Exibe a imagem
        echo '<img src="' . $img_path . '" alt="Imagem reconhecida">';
    } else {
        echo "Rosto não reconhecido.";
    }
}
?>
