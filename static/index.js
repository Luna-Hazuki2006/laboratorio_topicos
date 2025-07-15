function dar_radios() {
    let radios = document.querySelectorAll('input[type="radio"]')
    radios.item(0).checked = true
    let completo = document.getElementById('completo')
    let dividido = document.getElementById('dividido')
    dividido.classList.add('oculto')
    for (const radio of radios) {
        radio.addEventListener('click', (ev) => {
            if (radios.item(0).checked == true) {
                completo.classList.remove('oculto')
                dividido.classList.add('oculto')
            } else if (radios.item(1).checked == true) {
                completo.classList.add('oculto')
                dividido.classList.remove('oculto')
            }
            // completo.classList.toggle('oculto')
            // dividido.classList.toggle('oculto')
            if (location.pathname.includes('descuento')) {
                for (const cada of [completo, dividido]) {
                    let verdad = !cada.classList.contains('oculto')
                    let todos = cada.getElementsByTagName('input')
                    // radios.item(0).checked = verdad
                    // radios.item(1).checked = !verdad
                    for (const uno of todos) uno.required = verdad
                }
            }
        })
    }
}

function dar_post() {
    let datos_archivo = ''
    let archivo = document.getElementById('archivo')
    archivo.addEventListener('change', (ev) => {
        let lector = new FileReader()
        let dato = archivo.files[0]
        lector.onload = () => {
            datos_archivo = lector.result
            // .toString().replace('data:text/csv;', '');
        };
        lector.readAsText(dato)
        // lector.readAsDataURL(dato)
    })
    let forma = document.getElementById('abecedear')
    forma.addEventListener('submit', async (ev) => {
        ev.preventDefault()
        const d = new FormData(ev.target)
        let radios = document.querySelectorAll('input[type="radio"]')
        if (radios.item(0).checked && d.get('archivo').name == '') {
            alert('Tiene que cargar un archivo .csv')
        } else if (radios.item(1).checked && 
            (d.get('demandas').match(/\n/g) || []).length != (d.get('costos').match(/\n/g) || []).length 
            || (d.get('demandas').length == 0 && d.get('costos'))) {
            alert('Los dos campos tienen que tener el mismo tamaño de filas')
        }
        console.log(datos_archivo);
        
        const respuesta = await fetch('/abc', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*'
            }, 
            body: JSON.stringify({
                'visiones': d.get('visiones'), 
                'archivo': datos_archivo, 
                'nombres': d.get('nombres') || '',
                'demandas': d.get('demandas'), 
                'costos': d.get('costos')
            })
        })
        let verdad = false
        console.log(respuesta);
        if (respuesta.status == 200) {
            let cuerpo = await respuesta.json()
            console.log(cuerpo);
            let lista = (localStorage.getItem('abc')) ? JSON.parse(localStorage.getItem('abc')) : []
            lista.push(cuerpo)
            localStorage.setItem('abc', JSON.stringify(lista))
            verdad = true
        } else if (respuesta.status == 400) {
            let cuerpo = await respuesta.json()
            console.log(cuerpo);
            alert(cuerpo.detail)
        } else {
            alert('Algo salió mal y no se pudo subir la información')
        }
        if (verdad) location.pathname = '/abc_res'
    })
}

function llenar_abc() {
    let lista = JSON.parse(localStorage.getItem('abc'))
    let titulos = Object.keys(lista[lista.length - 1]['archivo'][0])
    let contenedor = document.getElementById('tabla')
    let tabla = document.createElement('table')
    let tr = document.createElement('tr')
    for (const este of titulos) {
        let th = document.createElement('th')
        th.innerText = este
        tr.appendChild(th)
    }
    tabla.appendChild(tr)
    for (const este of lista[lista.length - 1]['archivo']) {
        tr = document.createElement('tr')
        for (const cada of titulos) {
            let td = document.createElement('td')
            switch (cada) {
                case 'COSTO_TOTAL': td.innerText = Number(este[cada].toFixed(4)); break;
                case 'PORCENTAJES': td.innerText = `${Number(este[cada].toFixed(4))}%`; break;
                default: td.innerText = este[cada]; break;
            }
            tr.appendChild(td)
        }
        tabla.appendChild(tr)
    }
    contenedor.appendChild(tabla)
    let imagen = document.getElementById('imagen')
    imagen.src = lista[lista.length - 1]['imagen']
    imagen.alt = 'Tabla de ABC'
}

function agregar() {
    let datos = ['unidades', 'descuentos', 'almacenamiento', 'preparacion']
    let temp = document.getElementsByTagName("template")[0];
    let tabla = document.getElementById('info')
    let lista = tabla.getElementsByTagName('tr')
    let clon = temp.content.cloneNode(true);
    lista.item(lista.length - 1).parentNode.appendChild(clon)
    let numero = 1
    if (lista.length > 2) {
        let ultimo = lista.item(lista.length - 2).children.item(0).children.item(0).id
        console.log(ultimo);
        numero = Number(ultimo.substring(datos[0].length), ultimo.length - 1) + 1
    } else numero = 1
    let i = 0
    for (const dato of lista.item(lista.length - 1).getElementsByTagName('input')) {
        dato.id = datos[i] + numero
        dato.name = datos[i] + numero
        i++
    }
    let boton = lista.item(lista.length - 1).getElementsByTagName('button')[0];
    boton.addEventListener('click', (evento) => {
        boton.parentElement.parentElement.remove()
    })
}

function intento_obtencion() {
    let oscuro = document.getElementById('oscuro')
    let imagen = document.getElementById('imagen')
    if (!oscuro || !imagen) return
    let lista = (localStorage.getItem('descuento')) ? JSON.parse(localStorage.getItem('descuento')) : []
    console.log(oscuro.innerText);
    let info = JSON.parse(oscuro.innerText)
    console.log(info);
    lista.push({
        'info': info, 
        'imagen': imagen.src
    })
    localStorage.setItem('descuento', JSON.stringify(lista))
}

function recoger() {
    let info = document.getElementById('info')
    let anterior = document.getElementById('anterior')
    let probabilidad = document.getElementById('probabilidad')
    if (info && anterior && probabilidad) {
        let lista = (localStorage.getItem('colas')) ? JSON.parse(localStorage.getItem('colas')) : []
        lista.push({
            'info': JSON.parse(info.innerText), 
            'anterior': JSON.parse(anterior.innerText), 
            'probabilidad': JSON.parse(probabilidad.innerText)
        })
        localStorage.setItem('colas', JSON.stringify(lista))
    }
}

function main() {
    // console.log(JSON.parse(localStorage.getItem('abc')))
    // localStorage.removeItem('abc')
    if (location.pathname.includes('abc')) {
        dar_radios()
        dar_post()
        if (location.pathname.includes('abc_res')) {
            llenar_abc()
        }
    } else if (location.pathname.includes('descuento')) {
        dar_radios()
        intento_obtencion()
    } else if (location.pathname.includes('colas')) {
        recoger()
    } else if (location.pathname.includes('probabilidad')) {
        
    }
}

main()