
const App = {
    created() {
        setInterval(()=>{
            if (this.autoRefresh)
            this.snapshot()
        }, 200)
    },
    data() {
        return {
            counter: 0,
            autoRefresh: false
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
            ws.send(JSON.stringify({
                cmd: 'read'
            }))
        },
        setRange (dist) {
            ws.send(JSON.stringify({
                cmd: 'set',
                param: 'range',
                value: parseInt(dist)*1000
            }))
        },
        setIntTime3D (intTime) {
            ws.send(JSON.stringify({
                cmd: 'set',
                param: 'intTime3D',
                value: parseInt(intTime)
            }))
        }
    }
}

Vue.createApp(App).mount('#app')