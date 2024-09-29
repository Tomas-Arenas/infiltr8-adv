class IP {
    constructor(id, ip, selected = false) {
        this.id = id;          
        this.ip = ip;          
        this.selected = selected;
    }

    toggleSelected() {
        this.selected = !this.selected;
    }
}

export default IP;