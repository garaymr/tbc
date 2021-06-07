const mostrarMenu = () =>
{
	const menuH = document.querySelector('.menuH');
	const logo = document.querySelector('.MarcaLogo');
	const nav = document.querySelector('.opcionesNav');
	const opcionesNav = document.querySelectorAll('.opcionesNav li');

	//Mostrar el menú móvil
	menuH.addEventListener('click',()=>
	{
		nav.classList.toggle('nav-active');
		//Animacion opciones del menú móvil
	opcionesNav.forEach((link,index) =>{
		if(link.style.animation)
		{
			link.style.animation = ''
		}
		else
		{
			link.style.animation = `desvanecerNav 0.5s ease forwards ${index / 7 + 0.5}s`;
		}
	});


	//Animación menuH
	menuH.classList.toggle('toggle');

});


}

mostrarMenu();