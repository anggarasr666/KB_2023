const randomInt = (start, end) => {
    return Math.floor(Math.random() * (end-start+1)) + start
}

// Straight line distance
const getDistance = (a, b) => {
    let x = Math.abs(b.position[0] - a.position[0])
    let y = Math.abs(b.position[1] - a.position[1])
    let temp = Math.floor(Math.sqrt(x*x + y*y))
    return temp
}

const Edge = (des, dis) => ({
    destination: des,
    distance: dis
})

const Vertex = (post) => ({
    position: post,
    neighbors: []
})

const randomGraph = (MAX_VERT, AREA_SIZE) => {
    let adj = []
    // let vertices = randomInt(4,MAX_VERT)
    let vertices = MAX_VERT

    for(let i = 0; i < vertices; i++) {
        var x = randomInt(1, AREA_SIZE)
        var y = randomInt(1, AREA_SIZE)
        adj.push(Vertex([x, y]))
    }

    // Generate edges
    adj.map((val, idx) => {
        var num = randomInt(1, 2)

        for(let i = 0; i < num; i++) {
            var next = randomInt(0, vertices-1)
            var randomDistance = randomInt(0, AREA_SIZE/10)
            if(next == idx) continue
            if(val.neighbors.find((x) => x.destination == next)) continue
            var distance = getDistance(val, adj[next])
            val.neighbors.push(Edge(next, distance + randomDistance))
            adj[next].neighbors.push(Edge(idx, distance + randomDistance))
        }
    })
    return adj
}

const PriorityQueue = (comparator = (a, b) => a - b) => ({
    arr: [],
    size: 0,
    push: function(val) {
        this.arr.push(val)
        this.arr.sort(comparator)
        this.size++
    },
    pop: function() {
        if(this.size > 0) this.size--
        return this.arr.shift()
    }
}) 

const aStar = (adj, start, des) => {
    // Parent, Current, A* Score
    let visited = [[start, start, getDistance(adj[start], adj[des])]]
    pq = PriorityQueue((a, b) => a[2] - b[2])
    // Parent, Current, Cost, A* Score
    pq.push([start, start, 0, getDistance(adj[start], adj[des])])
    let path = []
    while(pq.size) {
        // Returns path
        if(path.length) return [path.reverse().slice(1,path.length), path[0]]
        var current = pq.pop()
        var parent = current[0]
        var node = current[1]
        var cost = current[2]
        var score = current[3]
        adj[node].neighbors.map((val) => {
            if(visited.find((x) => x[1] == val.destination) !== undefined) {
                // Update visited node if current path is shorter
                var visNode = visited.findIndex((x) => x[1] == val.destination)
                if(visited[visNode][2] > score) {
                    visited[visNode][0] = parent
                    visited[visNode][2] = score
                }
            } else {
                // Add neighbors to priority queue
                var newCost = cost + val.distance
                var newScore = newCost + getDistance(adj[des], adj[val.destination])
                visited.push([node, val.destination, newScore])
                pq.push([node, val.destination, newCost, newScore])
                // Ouput path
                if(val.destination == des) {
                    let prev = node
                    path.push(visited[visited.length-1][1])
                    for(let i = visited.length-1; i >= 0; i--) {
                        if(visited[i][1] == prev) {
                            path.push(visited[i][1])
                            prev = visited[i][0]
                        }
                    }
                    path.push(newCost)
                }
            }
        })
    }
    return [undefined, undefined]
}

adj = randomGraph(20, 50)
console.log(adj)
let [path, cost] = aStar(adj, 0, 11)
if(path) {
    console.log("Path : ")
    console.log(path)
    console.log("Total Cost : \n" + cost)
} else {
    console.log("Path not found!")
}
