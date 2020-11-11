
import * as Vue from  './vue.esm-browser.js'
import './pointsView.js'


const App = {
    created() {
        
        if (ws.readyState === 1) {
            this.setRange(this.viewDistance)
            this.setIntTime3D(this.intTime3D)
            this.loaded = true
        } else {
            ws.onopen = () => {
                this.setRange(this.viewDistance)
                this.setIntTime3D(this.intTime3D)
                this.loaded = true
            }
        }

        setInterval(()=>{
            if (this.autoRefresh)
            this.snapshot()

        }, 200)
    },
    data() {
        return {
            counter: 0,
            viewDistance: 4000,
            autoRotate: false,
            autoRefresh: true,
            intTime3D: 1000,
            loaded: false,
            showHelp: false
        }
    },
    methods: {
        pointSize (val) {
            if (val === 'up') {
                material.size = material.size + 0.01

            } else if (val === 'down') {
                material.size = material.size - 0.01
            }
        },
        resetView () {
            controls.reset()
        },
        snapshot () {
            ws.sendObj({
                cmd: 'read'
            })
        },
        setRange (e) {
            if (typeof(e) === 'object') var value = parseInt(e.target.value)
            else var value = e
            ws.sendObj({
                cmd: 'set',
                param: 'range',
                value: value
            })
            this.viewDistance = value
        },
        setIntTime3D (e) {
            if (typeof(e) === 'object') var value = parseInt(e.target.value)
            else var value = e
            ws.sendObj({
                cmd: 'set',
                param: 'intTime3D',
                value: value
            })
            this.intTime3D = value
        },
        onAutoRotate: function () {
            this.autoRotate = !this.autoRotate
            controls.autoRotate = this.autoRotate
        }
    },
    computed: {
    }
}

const app = Vue.createApp(App)


app.mount('#app')