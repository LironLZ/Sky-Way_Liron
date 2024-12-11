class LoginToken:
    @staticmethod
    def create_login_token(username: str, password: str) -> Optional['LoginToken']:
        """
        Create a login token if credentials are valid
        """
        session = SessionLocal()
        try:
            # Query to validate user and get their information
            result = session.execute(
                text("""
                    SELECT u.id, u.username, ur.role_name 
                    FROM users u
                    JOIN user_roles ur ON u.user_role = ur.id
                    WHERE u.username = :username AND u.password = :password
                """),
                {"username": username, "password": password}
            ).fetchone()
            
            if result:
                return LoginToken(
                    id=result.id,
                    name=result.username,
                    role=result.role_name
                )
            return None
        finally:
            session.close()

def create_facade_by_login(username: str, password: str):
    """
    Create appropriate facade based on login credentials
    Returns the appropriate facade with login token if credentials are valid
    """
    token = LoginToken.create_login_token(username, password)
    if not token:
        return None

    # Create appropriate facade based on role
    if token.role.lower() == "administrator":
        from facades import AdministratorFacade
        return AdministratorFacade(token)
    elif token.role.lower() == "airline":
        from facades import AirlineFacade
        return AirlineFacade(token)
    elif token.role.lower() == "customer":
        from facades import CustomerFacade
        return CustomerFacade(token)
    
    return None