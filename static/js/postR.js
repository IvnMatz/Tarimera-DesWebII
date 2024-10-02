document.getElementById('form').addEventListener('submit', async function (event) {
    event.preventDefault();  // evite el envio default
    
    const form = event.target;
    const formData = new FormData(form);  // Obtiene los datos del formulario
  
    try {
      // Realiza la petición POST
      const response = await fetch(form.action, {
        method: 'POST',
        body: formData
      });
  
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
  
      const result = await response.json(); // Asume que la respuesta es JSON
  
      // Verifica la respuesta para mostrar una alerta
      if(result.message){
      if (result.message === 'Vacia') {
        alert('No se puede envíar una reseña vacia');
      }
      else if (result.message === 'ok' ){
        location.reload();
      }
    }
  
    } catch (error) {
      console.error('Hubo un problema con la petición:', error);
    }
  });