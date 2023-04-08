// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
	// mapping( uint => uint[2][] ) public network;
	mapping( uint => string ) public users;
	
	uint[501][501] public network;
    function registerUser(uint user_id, string memory user_name) public {
		users[user_id] = user_name;	
    }

	function createAcc(uint user_id1, uint user_id2, uint amount1, uint amount2) public {
		// network[user_id1].push([user_id2,0]);
		// network[user_id2].push([user_id1,0]);
		network[user_id1][user_id2] = amount1;
		network[user_id2][user_id1] = amount2;
	}

	function sendAmount(uint user_id1, uint user_id2, uint amount) public {
		bool[501] memory visited;
		bool found = false;
		uint front = 0 ;
		uint rear  = 1 ;
		uint [501] memory parent;
		uint [501] memory qq;
		qq[1] = user_id1;
		parent[user_id1] = 0;
		while(front!=rear)
		{
			front+=1;
			uint node = qq[front];
			visited[node]= true;
			for(uint i=1 ; i<= 500 ; i++)
			{
				if(visited[i] || i==node || network[node][i]<amount)
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

		while(parent[node2]!=0)
		{
			uint pred = parent[node2];
			network[node2][pred]+=amount;
			network[pred][node2]-=amount;
			node2 = pred;
		} 

	}

	function closeAccount(uint user_id1, uint user_id2) public {

	}
}
