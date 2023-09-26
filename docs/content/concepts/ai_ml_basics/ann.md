


## Artificial Neural Networks

One method of machine learning involves utilising Artificial Neural Networks, which are designed to mimic the neural network of humans. They are primarily trained using a data-driven approach.

An Artificial Neural Network consists of simulated neurons, which are called nodes. Each node is connected to other nodes via links, similar to biological connections, and they form a 'graph'. Nodes that perform the same function are grouped into layers. Graphs can have different types of 'wiring' or connections based on their configuration. The overall structure and functioning of an Artificial Neural Network constitute its model.

We can also categorize cognitive functions as discriminative and generative. Depending on the function for which we train the network, we obtain either a discriminative model or a generative model.

!!! note "Discriminative"

	 The regression and classification functions are loosely referred to as discriminative.

### Node
A node serves as the fundamental unit in artificial neural networks. It processes input data through various mathematical operations like addition, multiplication, and activation functions such as sigmoid or ReLU, ultimately yielding an output. The specific mathematical operations carried out depend on the network's architecture and its intended purpose.

Here is the mathematical operations used by different networks.

=== "Feedforward Neural Network (FNN)"

	 \(y_t = f(\sum_{i=1}^{n} w_i \cdot x_{ti} + b)\)
	
	Where,

	  - \(y_t\) is the output at time step \(t\).
	  - \(f\) is the activation function.
	  - \(n\) is the number of input connections.
	  - \(w_i\) are the weights of the connections.
	  - \(x_{ti}\) are the inputs at time step \(t\).
	  - \(b\) is the bias term.

=== "Recurrent Neural Network (RNN)"

	\(h_t = f(\sum_{i=1}^{n} (W_{hx_i} \cdot x_{ti}) + \sum_{j=1}^{m} (W_{hh_j} \cdot h_{t-1j}) + b_h)\)
	
	\(y_t = g(\sum_{k=1}^{p} (W_{yk} \cdot h_{tk}) + b_y)\)
	
	Where,
	
	  - \(h_t\) is the hidden state at time step \(t\).
	  - \(x_{ti}\) is the input at time step \(t\) and feature \(i\).
	  - \(f\) is the activation function for the hidden state.
	  - \(n\) is the number of input features.
	  - \(W_{hx_i}\) is the weight associated with input \(i\) at time step \(t\).
	  - \(m\) is the number of input features.
	  - \(W_{hh_j}\) is the weight associated with the previous hidden state feature \(j\).
	  - \(b_h\) is the bias term for the hidden state.
	  - \(y_t\) is the output at time step \(t\).
	  - \(h_{tk}\) is the hidden state at time step \(t\) and feature \(k\).
	  - \(p\) is the number of output features.
	  - \(W_{yk}\) is the weight associated with hidden state feature \(k\) for output \(y_t\).
	  - \(b_y\) is the bias term for the output.
	  - \(g\) is the output activation function.

=== "Convolutional Neural Network (CNN)"

	\[y_{ijk} = f\left(\sum_{m=1}^{M} \sum_{n=1}^{N} \sum_{p=1}^{P} (w_{mnpk} \cdot x_{i+m-1, j+n-1, p}) + b_k\right)\]
	
	Where,
	
	- \(y_{ijk}\) is the output at spatial position \((i, j)\) for filter \(k\).
	- \(f\) is the activation function.
	- \(M\) is the width of the filter.
	- \(N\) is the height of the filter.
	- \(P\) is the depth of the filter (number of input channels).
	- \(w_{mnpk}\) are the weights of the filter for filter \(k\).
	- \(x_{i+m-1, j+n-1, p}\) are the input values.
	- \(b_k\) is the bias term for filter \(k\).

The bias  and weight matrices / convolutional filters are trainable parameters.

!!! info "Trainable Parameters"

	 Trainable parameters are initialized before training and updated while training as part of learning.
### Activation Function