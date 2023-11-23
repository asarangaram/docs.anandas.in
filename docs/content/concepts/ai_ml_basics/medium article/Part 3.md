### Artificial Intelligence — A Clear and Simple Introduction: Part 3

_This is the third part of five part introduction series on “Artificial Intelligence”, an attempt to explain the fundamentals in simple language without much technical jargon._

- _Read the first part_ [_here_](https://medium.com/@anandasarangaram/artificial-intelligence-a-clear-and-simple-introduction-part-1-0d5cc0bcec96)_._
- _Read the second part here._

> _From now on, we refer Artificial Narrow Intelligence as AI for simplicity._

### Rule based

An in-depth study of human problem-solving skills and attempts to formalize them marked the early stage of AI development. This led to the development of rule-based models.

Expert systems, which assist in decision-making from a knowledge base containing a large collection of rules (nested if-then-else statements) and facts about a specific domain, provide a good example of rule-based models. With input from many experts, the system was able to make decisions that mimicked human ones.

An example of an expert system is a “disease diagnostic system,” where possible diseases are identified by providing the symptoms. This works through deduction based on the symptoms provided. Another example is playing games like chess, where the possible moves are pre-programmed based on the expected opponent’s moves.

### Symbolic AI

Rule-based models are a part of Symbolic Artificial Intelligence (Symbolic AI), which focuses on finding improved methods to represent knowledge. Symbolic AI is the overarching term used to describe approaches that address problems in a format that is easily understandable to humans (using symbols to create expressions and then manipulate those symbols = programs).

The rule based systems was accurate, but suffered with the following drawbacks.

1. When a problem becomes exponentially more complex, a conventional knowledge-based system with slow algorithms tends to under-perform
2. These systems were entirely dependent on the accuracy and completeness of the defined rules. Apparently, they couldn’t adapt to new situations or facts that were not covered by them.

To over come this, many approaches were tried, by extending the logic of the rules or by passing the standard flow of rules.

A faster algorithm called Heuristics was designed to find an approximate solution more quickly, rather than exhaustively traversing the entire if-else rules. Heuristics involve rules of thumb that help bypass many unrelated rules. This can be conceptualized as rule-based algorithms with a hierarchical structure.

First-order logic is an another foundational tool to representing complex relationships and making precise statements about objects and their properties.

For the fields where the rules are impossible to define, for example on speech recognition, statistical modelling was tried. One of the popular model was Hidden Markov Model (HMM) that makes predictions based on patterns it sees.

Even though statistics was tried, the Symbolic AI represents the the knowledge using symbols, logic and expressions. It always uses a set of predefined rules to make decision. That means the reason for the decision is explainable and hence Symbolic AI approach is used in **Explainable AI,** for critical applications like healthcare and finance

Note, that introduction of statistic models and machine learning and with the rise of deep learning lead to a hybrid approach in which both rule based models and statistical models were used.

### Connectionist AI

Instead of representing cognitive functions through symbols and logic, an alternative approach emerged, which involved studying the human mental process and emulating it through an artificial brain that stores knowledge through connections.

AI systems developed by this approach is called Connectionist AI.

In this approach, the AI system is constructed as interconnected networks of artificial neurons (nodes), mirroring the structure of the human brain. These networks are known as neural networks.

This approach includes the development of various technologies such as perceptrons, Convolutional Neural Networks (CNNs), Transformers, and Generative Adversarial Networks (GANs), which uses deep learning techniques.

These AI systems are not programmed explicitly, instead they acquire knowledge through Machine Learning.

Although the advancement in Connectionist AI is significant, they still lack the ability to become Real AI or Artificial General Intelligence. As of today, both Symbolic AI and Connectionist AI exist as different philosophy. A hybrid AI system called neuro-symbolic AI is also evolving. The earlier Symbolic AI that don’t use neural networks is called “Good Old-Fashioned AI” (GOFAI).

_What is deep learning? How is Connectionist AI modeling achieved using deep neural networks and trained by machine learning techniques? Let us continue in the next part._