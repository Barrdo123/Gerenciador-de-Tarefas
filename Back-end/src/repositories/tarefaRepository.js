const Tarefa = require('../models/tarefa');
class TarefaRepository {
    async getAllTarefas() {
        try {
            return await Tarefa.findAll();
        } catch (error) {
            throw new Error('Erro ao buscar todas as tarefas: ' + error.message);
        }
    }
    async createTarefa(tarefaData) {
        try {
            return await Tarefa.create(tarefaData);
        } catch (error) {
            throw new Error('Erro ao criar nova tarefa: ' + error.message);
        }
    }

    async getTarefaById(id){
        try {
            return await Tarefa.findByPk(id);
        } catch (error) {
            throw new Error('Erro ao encontrar tarefa: ' + error.message)
        }
    }

    async updateTarefa(id, dados) {
        try {
            const [rowsUpdated] = await Tarefa.update(dados, {
                where: { id }
            });

            if (rowsUpdated === 0) {
                throw new Error("Tarefa não encontrada ou dados iguais ao existente.");
            }

            return await this.getTarefaById(id);
        } catch (error) {
            throw new Error('Erro ao atualizar tarefa: ' + error.message);
        }
    }

    async deleteTarefa(id){
        if(id<=0){
            throw new Error('ID invalido')
        }
        try{

            const rowsDeleted =  await Tarefa.destroy({where: {id}});

            if(rowsDeleted === 0){
                throw new Error('Tarefa não encontrada: ')
            }

        } catch (error){

            throw new Error('Erro ao deletar tarefa: ' + error.message)
        }
    }
}
module.exports = new TarefaRepository();
