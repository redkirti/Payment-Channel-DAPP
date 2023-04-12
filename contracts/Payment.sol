// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
	// Mapping to store users with id as index
	mapping( uint => string ) public users;		
	// Event to check if a payment was successful
	event myEvent(bool found);
	// 2d array to store the entire network
	uint[110][110] public network;

	// Function to register a new user
    function registerUser(uint user_id, string memory user_name) public {
		users[user_id] = user_name;	
    }

	// Function to create a payment channel between two nodes
	function createAcc(uint user_id1, uint user_id2, uint amount) public {
		// Check if both users are registered
		require(keccak256(abi.encodePacked(users[user_id1])) !=  keccak256(abi.encodePacked("")));
		require(keccak256(abi.encodePacked(users[user_id2])) !=  keccak256(abi.encodePacked("")));
		network[user_id1][user_id2] = amount/2;
		network[user_id2][user_id1] = amount/2;
	}

	// Function to send amount from one node to other using bfs
	function sendAmount(uint user_id1, uint user_id2) public {
		bool[110] memory visited;
		bool found = false;
		uint front = 0 ;
		uint rear  = 1 ;
		uint [110] memory parent;
		uint [1100] memory qq;
		qq[1] = user_id1;
		parent[user_id1] = 0;
		while(front!=rear)
		{
			front+=1;
			uint node = qq[front];
			visited[node]= true;
			for(uint i=1 ; i<= 100 ; i++)
			{
				// Add to queue only if sender has enough liquidity in the payment channel
				if(visited[i] || i==node || network[node][i]<1)
					continue;
				rear+=1;
				qq[rear]= i;
				parent[i]=node;
				if(i==user_id2)
				{
					front=rear;
					found = true;
					break;
				}
			}
		}

		uint node2 = user_id2;
		// Make changes in the entire path in the network
		while(parent[node2]!=0)
		{
			uint pred = parent[node2];
			network[node2][pred]+=1;
			network[pred][node2]-=1;
			node2 = pred;
		} 
		emit myEvent(found);
	}

	// Function to close account
	function closeAccount(uint user_id1, uint user_id2) public {
		network[user_id1][user_id2] = 0;
		network[user_id2][user_id1] = 0;
	}
}
