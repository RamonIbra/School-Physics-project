import pygame
import numpy as np
import matplotlib.pyplot as plt

# Fysikkonstanter
k: float = 8.9875517873681764e9  # Coulombs konstant
m_proton: float = 1.6726219e-27  # Protonens massa
m_electron: float = 9.10938356e-31  # Elektronens massa
proton_charge: float = 1.602176634e-19  # Protonens laddning
electron_charge: float = -1.602176634e-19  # Elektronens laddning

# Initiala positioner och hastigheter för protoner och elektroner
# Dessa kan ändras för att testa olika scenarier

position_proton:np.float64 = np.array([200, 280], dtype='float64')
position_electron:np.float64 = np.array([600, 330], dtype='float64')
velocity_proton:np.float64 = np.array([1, 0], dtype='float64')
velocity_electron:np.float64 = np.array([-1, 0], dtype='float64')

# position_proton: np.float64 = np.array([200, 285], dtype='float64')
# position_electron: np.float64 = np.array([200, 350], dtype='float64')
# velocity_proton: np.float64 = np.array([1, 0], dtype='float64')
# velocity_electron: np.float64 = np.array([-1, 0], dtype='float64')


# Funktion för att beräkna Coulombs kraft mellan två partiklar
def Coulombs_force(pos_p: np.float64, pos_e: np.float64, charge_p: float, charge_e: float, object: str) -> np.float64:
    # Beräknar kraftriktningen beroende på om objektet är en elektron eller proton
    if object == 'e':
        r_vector: np.float64 = pos_e - pos_p
    elif object == 'p':
        r_vector: np.float64 = pos_p - pos_e
    r: float = np.linalg.norm(r_vector)
    r_hat: np.float64 = r_vector / r

    # Tillämpar Coulombs lag
    return ((k * charge_p * charge_e) / r**2) * r_hat

# Alternativ implementation av Coulombs kraftberäkning
def Coulombs_force2(pos_p: np.float64, pos_e: np.float64, charge_p: float, charge_e: float) -> np.float64:
    r_vector: np.float64 = pos_e - pos_p
    r: float = np.linalg.norm(r_vector)
    r_hat: np.float64 = r_vector / r

    # Tillämpar Coulombs lag
    return ((k * charge_p * charge_e) / r**2) * r_hat

# Leapfrog-metoden för att stegvis uppdatera positioner och hastigheter
def leapfrog_step(position_proton, position_electron, velocity_proton, velocity_electron, proton_charge, electron_charge, dt):
    # Beräknar kraften på varje partikel
    force_on_e = Coulombs_force(position_proton, position_electron, proton_charge, electron_charge, 'e')
    force_on_p = Coulombs_force(position_proton, position_electron, proton_charge, electron_charge, 'p')

    # Beräknar acceleration och ny hastighet
    acc_e = force_on_e / m_electron
    v_e = velocity_electron + acc_e * dt
    new_pos_e = position_electron + (velocity_electron * dt) + ((acc_e * (dt ** 2)) / 2)

    acc_p = force_on_p / m_proton
    v_p = velocity_proton + acc_p * dt
    new_pos_p = position_proton + (velocity_proton * dt) + ((acc_p * (dt ** 2)) / 2)

    return new_pos_p, new_pos_e, v_p, v_e

# Huvudprogrammet
if __name__ == "__main__":
    # Initiera Pygame och skapa fönstret
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Huvudloopen för simuleringen
    running = True
    dt = 0.1  # Tidssteg för simuleringen
    xpos: list[float] = []  # Lista för att spara x-positioner
    ypos: list[float] = []  # Lista för att spara y-positioner
    time: float = 0.0  # Simuleringstid
    while running:
        xpos.append(velocity_proton[0])
        ypos.append(velocity_proton[1])
        time = time + dt
        print(f'proton: {position_proton}, electron: {position_electron}, time: {time}')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Beräkna och uppdatera positioner/hastigheter med Leapfrog
        position_proton, position_electron, velocity_proton, velocity_electron = leapfrog_step(position_proton, position_electron, velocity_proton, velocity_electron, proton_charge, electron_charge, dt)

        # Rita partiklarna
        screen.fill((0, 0, 0))  # Svart bakgrund
        pygame.draw.circle(screen, (0, 0, 255), position_proton.astype(int), 7)  # Rita proton
        pygame.draw.circle(screen, (255, 255, 0), position_electron.astype(int), 3)  # Rita elektron

        pygame.display.flip()
        if time >= 800.0:
            pygame.quit()
            plt.plot(xpos)
            #plt.ylabel('some numbers')
            plt.show()
    

