from sigma_app import create_app


def test_auth_flow_and_index_rendering(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(tmp_path / "test.db"),
            "SECRET_KEY": "test-secret-key",
        }
    )

    with app.test_client() as client:
        cadastros_response = client.get("/cadastros")
        register_response = client.post(
            "/register",
            data={
                "leader_name": "lucas",
                "sector": "Manutencao",
                "password": "secret123",
                "confirm_password": "secret123",
            },
            follow_redirects=True,
        )
        logout_response = client.post("/logout", follow_redirects=True)
        login_response = client.post(
            "/login",
            data={"leader_name": "lucas", "password": "secret123"},
            follow_redirects=True,
        )
        index_response = client.get("/")

    assert cadastros_response.status_code == 200
    assert "Cadastros" in cadastros_response.data.decode("utf-8")
    assert "Cadastrar lider" in cadastros_response.data.decode("utf-8")
    assert register_response.status_code == 200
    assert "Cadastro realizado com sucesso." in register_response.data.decode("utf-8")
    assert logout_response.status_code == 200
    assert "Voce saiu do sistema." in logout_response.data.decode("utf-8")
    assert login_response.status_code == 200
    assert "Login realizado com sucesso." in login_response.data.decode("utf-8")
    assert index_response.status_code == 200
    assert "Bem-vindo, lucas do setor Manutencao" in index_response.data.decode("utf-8")