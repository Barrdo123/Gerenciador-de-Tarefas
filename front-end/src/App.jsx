import { useState, useEffect } from "react";
import axios from "axios";
import { ThemeProvider } from "styled-components";

import defaultTheme from "./themes/defaultTheme";

import Tarefa from "./components/Tarefa";
import Titulo from "./components/Titulo";
import Layout from "./components/Layout";
import NovaTarefaForm from "./components/NovaTarefaForm";
function App() {
  const [tarefas, setTarefas] = useState([]);
  const [novaTarefa, setNovaTarefa] = useState("");
  const [descricao, setDescricao] = useState("");
  const [idEditando, setIdEditando] = useState(null);

  const buscarTarefas = async () => {
    try {
      const response = await axios.get("http://localhost:3000/tarefas");
      setTarefas(response.data);
    } catch (error) {
      console.error("Erro ao buscar tarefas:", error);
    }
  };

  const concluirTarefa = async (id, concluidaAtual) => {
    try {
      await axios.put(`http://localhost:3000/tarefas/${id}`, {
        concluida: !concluidaAtual,
      });
      buscarTarefas();
    } catch (error) {
      console.error("Erro ao concluir tarefa:", error);
    }
  };

  const adicionarTarefa = async () => {
    if (novaTarefa.trim() === "") return;

    try {
      await axios.post("http://localhost:3000/tarefas", {
        titulo: novaTarefa,
        descricao,
        concluida: false,
      });

      buscarTarefas();
      setNovaTarefa("");
      setDescricao("");
    } catch (error) {
      console.error("Erro ao adicionar tarefa:", error);
    }
  };

  const deleteTarefa = async (id) => {
    try {
      await axios.delete(`http://localhost:3000/tarefas/${id}`);
      buscarTarefas();
    } catch (error) {
      console.log("Erro ao deletar tarefa", error);
    }
  };

  const updateTarefa = async (id, novoTitulo, novaDescricao) => {
    try {
      await axios.put(`http://localhost:3000/tarefas/${id}`, {
        titulo: novoTitulo,
        descricao: novaDescricao,
      });

      buscarTarefas();
      setIdEditando(null);
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
    }
  };

  useEffect(() => {
    buscarTarefas();
  }, []);

  return (
    <ThemeProvider theme={defaultTheme}>
      <Layout>
        <h1>Gerenciador de Tarefas </h1>

        <Titulo texto="Lista de Tarefas" />
        <ul>
          {tarefas.map((tarefa) => (
            <Tarefa
              key={tarefa.id}
              nome={tarefa.titulo}
              descricao={tarefa.descricao}
              concluida={tarefa.concluida}
              isEditando={idEditando === tarefa.id}
              onEditar={() => setIdEditando(tarefa.id)}
              onSalvar={(novoTitulo, novaDescricao) =>
                updateTarefa(tarefa.id, novoTitulo, novaDescricao)
              }
              onConcluir={() => concluirTarefa(tarefa.id, tarefa.concluida)}
              onDelete={() => deleteTarefa(tarefa.id)}
            />
          ))}
        </ul>

        <NovaTarefaForm
          novaTarefa={novaTarefa}
          descricao={descricao}
          setNovaTarefa={setNovaTarefa}
          setDescricao={setDescricao}
          onAdicionar={adicionarTarefa}
        />
      </Layout>
    </ThemeProvider>
  );
}

export default App;
