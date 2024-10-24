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

  document.getElementById('save').addEventListener('submit', async function (event) {
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
       if (result.message === 'saved' ){
        alert("Producto Guardado en Perfil")
      }
      else if(result.message === 'deleted'){
        alert("Producto borrado de Perfil")
      }
    }
  
    } catch (error) {
      console.error('Hubo un problema con la petición:', error);
    }
  });

  document.getElementById('cart').addEventListener('submit', async function (event) {
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
      if (result.message === 'agregado') {
        alert('Producto agregado al carrito');
      }
      if (result.message === 'NoSession') {
        alert('Favor de iniciar Sesión');
      }
    }
  
    } catch (error) {
      console.error('Hubo un problema con la petición:', error);
    }
  });