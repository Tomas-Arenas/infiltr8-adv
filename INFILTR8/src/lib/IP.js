class IP {
    constructor(id, ip, selected = false) {
        this.id = id;          
        this.ip = ip;          
        this.selected = selected;
    }

    toggleSelected() {
        this.selected = !this.selected;
    }

    // Method to get a description of the IP
    getDescription() {
        return `IP ID: ${this.id}, IP Address: ${this.ip}, Selected: ${this.selected}`;
    }
}

export default IP;