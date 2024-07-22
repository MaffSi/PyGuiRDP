# Importação dos módulos necessários
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5 import uic, QtCore
import configparser
from PyQt5.QtWidgets import QDesktopWidget

# Função para criar um arquivo de configuração com o endereço do servidor RDP
def createConf(rdp_server):
    # Cria um objeto ConfigParser
    configuration_file = configparser.ConfigParser()
    # Adiciona o endereço do servidor RDP à seção 'General' do arquivo de configuração
    configuration_file['General'] = {'RdpServer':rdp_server}
    
    # Escreve as configurações no arquivo config.ini
    with open('config.ini','w') as configfile:
        configuration_file.write(configfile)

# Função para ler o endereço do servidor RDP do arquivo de configuração
def readConf(config_file):
    # Cria um objeto ConfigParser
    configuration_file = configparser.ConfigParser()  
    # Lê o arquivo de configuração config.ini
    configuration_file.read('config.ini')
    # Retorna o endereço do servidor RDP armazenado na seção 'General'
    return configuration_file.get('General','RdpServer')

# Classe da janela de login RDP
class RDPLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        self.load_ui()



        self.setStyleSheet("""
            QLineEdit, QPushButton { /* Seleciona filhos diretos da QMainWindow */
                background-color: white;
                border-style: outset;
                border-width: 2px;
                border-color: darkgray;
            }

        """)

    # Carregar a interface do usuário
    def load_ui(self):
        # Carrega a interface de usuário definida no arquivo LogIn.ui
        uic.loadUi("LogIn.ui", self)
        # Preenche o campo de endereço do servidor com o valor lido do arquivo de configuração
        self.ServidorURL.setText(readConf('config.ini'))
        # Conecta os sinais de pressionar 'Enter' nos campos de texto aos métodos correspondentes
        self.Password.returnPressed.connect(self.on_login_button_clicked)
        # Conecta o sinal de clique no botão 'Entrar' ao método correspondente
        self.Entrar.clicked.connect(self.on_login_button_clicked)
        # Conecta o sinal de clique no botão 'Config' ao método correspondente
        self.Config.clicked.connect(self.config_ui)


    # Configurar a interface do usuário para inserir o endereço do servidor
    def config_ui(self):
        # Abre um diálogo para inserir o endereço do servidor
        url, ok = QInputDialog().getText(self,'Configuração', 'Insira o endereço do servidor:')
        # Se o usuário inseriu um endereço e confirmou, atualiza o campo de endereço do servidor e cria/atualiza o arquivo de configuração
        if ok:
            self.ServidorURL.setText(str(url))
            createConf(str(url))
            
    
    # Conectar-se ao servidor RDP
    def connect_to_rdp(self, username, password):
        # Verifica se o arquivo de configuração existe e lê o endereço do servidor RDP dele
        if os.path.exists('config.ini'):
            rdp_server = readConf('config.ini')
        else:
            rdp_server = ''
        rdp_username = username

        # Constrói o comando xfreerdp com o endereço do servidor, nome de usuário e senha fornecidos
        command = [
            "xfreerdp",
            "/v:" + rdp_server,
            "/u:" + rdp_username,
            "/p:" + password,
            "/floatbar:sticky:on,default:visible,show:fullscreen",
            "/f",
	        "/dynamic-resolution",
            "/printer",
            "/cert-ignore",  # Ignorar erros de certificado (opcional)
            "+gfx-thin-client",
	        "+aero",
            "+auto-reconnect",
            "+clipboard"
        ]

        # Inicia o processo xfreerdp
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.close()
            if "STATUS_LOGON_FAILURE" in result.stdout:
                QMessageBox.critical(None, "Error", "Credenciais inválidas!")
        except subprocess.CalledProcessError as e:
            # Exibe uma mensagem de erro em caso de falha na conexão
            QMessageBox.critical(None, "Error", f"Failed to connect: {e}")

    # Lidar com o clique no botão de login
    def on_login_button_clicked(self):
        # Obtém o nome de usuário e senha digitados pelo usuário
        username = self.User.text()
        password = self.Password.text()

        # Se ambos os campos de nome de usuário e senha estiverem preenchidos
        if username and password:
            # Conecta-se ao servidor RDP com as credenciais fornecidas
            self.connect_to_rdp(username, password)
            # Limpa os campos de nome de usuário e senha após a tentativa de login
            self.User.clear()
            self.Password.clear()
        else:
            # Se um ou ambos os campos estiverem vazios, exibe uma mensagem de aviso
            QMessageBox.warning(None, "Warning", "Insira seu nome de usuário e senha!")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
# Função principal
def main():
    # Inicia a aplicação PyQt5
    app = QApplication(sys.argv)
    # Cria uma instância da janela de login RDP
    window = RDPLoginWindow()
    window.center()
    # Oculta a barra de título da janela
#    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    # Exibe a janela de login
    window.show()
    # Executa o loop de eventos da aplicação
    sys.exit(app.exec())

# Verificar se o script está sendo executado como o programa principal
if __name__ == "__main__":
    # Chama a função principal para iniciar o aplicativo
    main()
