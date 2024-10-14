#include <iostream>
#include <vector>
#include <random>
#include <deque>
#include <unordered_set>
#include <cmath>
#include <fstream>
#include <functional>
#include <algorithm>
#include<memory>

class Graph {
public:
    std::vector<std::vector<int>> edges;
    int n;

    Graph(int n) : n(n) {
        possible_edges.reserve(n * (n - 1) / 2);
        for (int u = 0; u < n; ++u) {
            for (int v = u + 1; v < n; ++v) {
                possible_edges.emplace_back(std::make_pair(u, v));
            }
        }
        edges.resize(n);
    }

    void add_edge(int u, int v) {
        edges[u].push_back(v);
        edges[v].push_back(u);
    }

protected:
    std::vector<std::pair<int, int>> possible_edges;
};

class UniformGraph : public Graph {
public:
    std::string name;

    UniformGraph(int n, int m) : Graph(n) {
        generate_uniform_edges(m);
        name = "uniform";
    }

    void generate_uniform_edges(int m) {
        std::random_device rd;
        std::mt19937 g(rd());

        if (m > possible_edges.size()) {
            std::cerr << "Error: m > possible_edges.size()\n";
            throw std::invalid_argument("Too many edges requested.");
        }

        std::shuffle(possible_edges.begin(), possible_edges.end(), g);

        for (int i = 0; i < m; ++i) {
            add_edge(possible_edges[i].first, possible_edges[i].second);
        }
    }
};

class BinomialGraph : public Graph {
public:
    std::string name;

    BinomialGraph(int n, double p) : Graph(n) {
        generate_binomial_edges(p);
        name = "binomial";
    }

    void generate_binomial_edges(double p) {
        std::random_device rd;
        std::mt19937 g(rd());
        std::uniform_real_distribution<> dist(0.0, 1.0);

        for (const auto &edge : possible_edges) {
            if (dist(g) < p) {
                add_edge(edge.first, edge.second);
            }
        }
    }
};

bool has_at_least_one_triangle(const Graph &g) {
    for (int v1 = 0; v1 < g.edges.size(); ++v1) {
        for (int v2 : g.edges[v1]) {
            for (int v3 = 0; v3 < g.edges.size(); ++v3) {
                if (std::find(g.edges[v3].begin(), g.edges[v3].end(), v1) != g.edges[v3].end() &&
                    std::find(g.edges[v3].begin(), g.edges[v3].end(), v2) != g.edges[v3].end()) {
                    return true;
                }
            }
        }
    }
    return false;
}

bool is_connected(const Graph &g) {
    std::deque<int> queue{0};
    std::unordered_set<int> visited{0};

    while (!queue.empty()) {
        int v = queue.front();
        queue.pop_front();
        for (int neighbor : g.edges[v]) {
            if (visited.find(neighbor) == visited.end()) {
                queue.push_back(neighbor);
                visited.insert(neighbor);
            }
        }
    }

    return visited.size() == g.n;
}

bool has_half_of_vertices_with_degree_4(const Graph &g) {
    int count = 0;
    for (const auto &edges : g.edges) {
        if (edges.size() >= 4) {
            count++;
        }
    }
    return count >= g.n / 2;
}

bool has_amount_edges_different_than_m(int m, const Graph &g) {
    int edge_count = 0;
    for (const auto &edges : g.edges) {
        edge_count += edges.size();
    }
    return m != edge_count / 2;
}

double binom_n_2(int n) {
    return n * (n - 1) / 2.0;
}

// Assume that other necessary functions and classes (Graph, UniformGraph, BinomialGraph, etc.) are already defined above

void main_loop() {
    std::vector<int> ns_tested = {5};
    for (int i = 10; i < 400; i += 50) {
        ns_tested.push_back(i);
    }

    std::vector<std::pair<std::function<double(int)>, std::string>> possible_ms = {
        {[](int n) { return std::sqrt(n); }, "sqrt(n)"},
        {[](int n) { return n; }, "n"},
        {[](int n) { return 2 * n; }, "2n"},
        {[](int n) { return n * std::log2(n); }, "n*log2(n)"},
        {[](int n) { return (1 / 4.0) * n * n; }, "1/4n^2"}
    };

    std::string print_string;

    for (const auto &[possible_m, m_name] : possible_ms) {
        for (int n : ns_tested) {
            int m = static_cast<int>(possible_m(n));
            if (m > binom_n_2(n)) {
                continue;
            }
            double p = m / binom_n_2(n);

            std::vector<std::function<bool(const Graph &)>> features = {
                has_at_least_one_triangle,
                is_connected,
                has_half_of_vertices_with_degree_4,
                [m](const Graph &g) { return has_amount_edges_different_than_m(m, g); }
            };

            std::cout << "Doing tests for n=" << n << ", m=" << m << std::endl;

            // Loop through graph types using strings
            std::vector<std::string> graph_types = {"uniform", "binomial"};

            const int AMOUNT_TESTS = 100;
            for (const auto& graph_type : graph_types) {
                // Store results for each feature
                std::vector<double> feature_results(features.size(), 0.0);

                // Run the tests and generate a new graph for each iteration
                for (int i = 0; i < AMOUNT_TESTS; ++i) {
                    std::shared_ptr<Graph> graph;

                    // Create a new graph for each test iteration
                    if (graph_type == "uniform") {
                        graph = std::make_shared<UniformGraph>(n, m);
                    } else if (graph_type == "binomial") {
                        graph = std::make_shared<BinomialGraph>(n, p);
                    }

                    // Evaluate all features for the generated graph
                    for (size_t j = 0; j < features.size(); ++j) {
                        feature_results[j] += features[j](*graph);
                    }
                }

                // Calculate averages
                for (auto &result : feature_results) {
                    result /= AMOUNT_TESTS;
                }

                // Append results to print_string
                print_string += std::to_string(n) + " " + m_name + " " + graph_type + " ";
                for (double result : feature_results) {
                    print_string += std::to_string(result) + " ";
                }
                print_string += "\n";
            }
        }
    }

    // Write results to file
    std::ofstream file("data.txt");
    if (file.is_open()) {
        file << print_string;
        file.close();
    } else {
        std::cerr << "Unable to open file data.txt\n";
    }
}

int main() {
    main_loop();
    return 0;
}
