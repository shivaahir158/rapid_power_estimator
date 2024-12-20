#
#  Copyright (C) 2024 RapidSilicon
#  Authorized use only

import pytest
from unittest.mock import MagicMock, patch
from device.device_resource import ResourceAttributes
from submodule.rs_power_config import ElementType
from submodule.rs_device_resources import (
    RsDeviceResources,
    IO_Standard_Coeff,
    IO_Standard,
    IO_BankType,
    PeripheralType,
    ModuleType,
    DeviceNotFoundException,
)

@pytest.fixture
def mock_device():
    device = MagicMock()
    device.series = 'Gemini'
    device.name = 'TestDevice'
    device.package = 'TestPackage'
    device.speedgrade = 'Speed1'
    device.filepath = 'device.xml'
    device.resources = {
        "dsp": ResourceAttributes(type='dsp', num=176, label='DSP'),
        "bram": ResourceAttributes(type='bram', num=176, label='BRAM'),
        "lut": ResourceAttributes(type='lut', num=45408, label='LUTs')
    }
    return device

@pytest.fixture
def device_resources(mock_device):
    with patch('submodule.rs_device_resources.RsPowerConfig') as MockRsPowerConfig:
        MockRsPowerConfig.return_value.load.return_value = True
        yield RsDeviceResources(mock_device)

def test_get_device_name(device_resources):
    assert device_resources.get_device_name() == 'TestDevice'

def test_get_series(device_resources):
    assert device_resources.get_series() == 'Gemini'

def test_get_package(device_resources):
    assert device_resources.get_package() == 'TestPackage'

def test_get_speedgrade(device_resources):
    assert device_resources.get_speedgrade() == 'Speed1'

def test_get_num_PLLs(device_resources):
    assert device_resources.get_num_PLLs() == 4  # Since series is 'Gemini'

def test_get_num_DSP_BLOCKs(device_resources):
    assert device_resources.get_num_DSP_BLOCKs() == 176

def test_get_num_18K_BRAM(device_resources):
    assert device_resources.get_num_18K_BRAM() == 352  # 176 * 2

def test_get_num_36K_BRAM(device_resources):
    assert device_resources.get_num_36K_BRAM() == 176

def test_get_num_LUTs(device_resources):
    mock_device = device_resources.device
    mock_device.resources = {'lut': MagicMock(num=100)}
    assert device_resources.get_num_LUTs() == 100

def test_get_num_FFs(device_resources):
    mock_device = device_resources.device
    mock_device.resources = {'ff': MagicMock(num=200)}
    assert device_resources.get_num_FFs() == 200

def test_get_num_CLBs(device_resources):
    assert device_resources.get_num_CLBs() == 5676

def test_register_module(device_resources):
    module = MagicMock()
    device_resources.register_module(ModuleType.CLOCKING, module)
    assert device_resources.get_module(ModuleType.CLOCKING) == module

def test_get_clock_not_found(device_resources):
    device_resources.register_module(ModuleType.CLOCKING, MagicMock(get_all=MagicMock(return_value=[])))
    assert device_resources.get_clock('non_existent_clock') is None

@pytest.mark.parametrize("method_name, element_type, coef_name, coef_value", [
    ("get_UART_CLK_FACTOR", ElementType.UART, "UART_CLK_FACTOR", 0.1234),
    ("get_UART_SWITCHING_FACTOR", ElementType.UART, "UART_SWITCHING_FACTOR", 0.4567),
    ("get_UART_IO_FACTOR", ElementType.UART, "UART_IO_FACTOR", 123.456),
    ("get_QSPI_CLK_FACTOR", ElementType.SPI, "QSPI_CLK_FACTOR", 0.1234),
    ("get_QSPI_SWITCHING_FACTOR", ElementType.SPI, "QSPI_SWITCHING_FACTOR", 0.4567),
    ("get_QSPI_IO_FACTOR", ElementType.SPI, "QSPI_IO_FACTOR", 123.456),
    ("get_ACPU_CLK_FACTOR", ElementType.ACPU, "ACPU_CLK_FACTOR", 0.1111111),
    ("get_ACPU_LOW_LOAD_FACTOR", ElementType.ACPU, "ACPU_LOW_LOAD_FACTOR", 0.1234),
    ("get_ACPU_MEDIUM_LOAD_FACTOR", ElementType.ACPU, "ACPU_MEDIUM_LOAD_FACTOR", 0.4567),
    ("get_ACPU_HIGH_LOAD_FACTOR", ElementType.ACPU, "ACPU_HIGH_LOAD_FACTOR", 123.456),
    ("get_BCPU_CLK_FACTOR", ElementType.BCPU, "BCPU_CLK_FACTOR", 1111.2222),
    ("get_BCPU_LOW_LOAD_FACTOR", ElementType.BCPU, "BCPU_LOW_LOAD_FACTOR", 0.456),
    ("get_BCPU_MEDIUM_LOAD_FACTOR", ElementType.BCPU, "BCPU_MEDIUM_LOAD_FACTOR", 0.123),
    ("get_BCPU_HIGH_LOAD_FACTOR", ElementType.BCPU, "BCPU_HIGH_LOAD_FACTOR", 123.456),
    ("get_JTAG_CLK_FACTOR", ElementType.JTAG, "JTAG_CLK_FACTOR", 0.4321),
    ("get_JTAG_SWITCHING_FACTOR", ElementType.JTAG, "JTAG_SWITCHING_FACTOR", 0.8765),
    ("get_JTAG_IO_FACTOR", ElementType.JTAG, "JTAG_IO_FACTOR", 85.9087),
    ("get_I2C_CLK_FACTOR", ElementType.I2C, "I2C_CLK_FACTOR", 0.4321),
    ("get_I2C_SWITCHING_FACTOR", ElementType.I2C, "I2C_SWITCHING_FACTOR", 0.8765),
    ("get_I2C_IO_FACTOR", ElementType.I2C, "I2C_IO_FACTOR", 85.9087),
    ("get_USB2_CLK_FACTOR", ElementType.USB2, "USB2_CLK_FACTOR", 0.4321),
    ("get_USB2_SWITCHING_FACTOR", ElementType.USB2, "USB2_SWITCHING_FACTOR", 0.8765),
    ("get_USB2_IO_FACTOR", ElementType.USB2, "USB2_IO_FACTOR", 85.9087),
    ("get_GIGE_CLK_FACTOR", ElementType.GIGE, "GIGE_CLK_FACTOR", 0.421),
    ("get_GIGE_SWITCHING_FACTOR", ElementType.GIGE, "GIGE_SWITCHING_FACTOR", 0.865),
    ("get_GIGE_IO_FACTOR", ElementType.GIGE, "GIGE_IO_FACTOR", 8.987),
    ("get_GPIO_CLK_FACTOR", ElementType.GPIO, "GPIO_CLK_FACTOR", 0.21),
    ("get_GPIO_SWITCHING_FACTOR", ElementType.GPIO, "GPIO_SWITCHING_FACTOR", 0.85),
    ("get_GPIO_IO_FACTOR", ElementType.GPIO, "GPIO_IO_FACTOR", 8.97),
    ("get_DDR_CLK_FACTOR", ElementType.DDR, "DDR_CLK_FACTOR", 8.987),
    ("get_DDR_WRITE_FACTOR", ElementType.DDR, "DDR_WRITE_FACTOR", 0.21),
    ("get_DDR_READ_FACTOR", ElementType.DDR, "DDR_READ_FACTOR", 0.85),
    ("get_DDR_ACLK_FACTOR", ElementType.DDR, "DDR_ACLK_FACTOR", 8.97),
    ("get_SRAM_WRITE_FACTOR", ElementType.SRAM, "SRAM_WRITE_FACTOR", 0.121),
    ("get_SRAM_READ_FACTOR", ElementType.SRAM, "SRAM_READ_FACTOR", 0.285),
    ("get_SRAM_ACLK_FACTOR", ElementType.SRAM, "SRAM_ACLK_FACTOR", 8.397),
    ("get_PWM_IO_FACTOR", ElementType.PWM, "PWM_IO_FACTOR", 123.456),
    ("get_VCC_CORE", ElementType.REGULATOR, "VCC_CORE", 1.397),
    ("get_VCC_AUX", ElementType.REGULATOR, "VCC_AUX", 2.397),
    ("get_VCC_BOOT_IO", ElementType.REGULATOR, "VCC_BOOT_IO", 3.397),
    ("get_VCC_DDR_IO", ElementType.REGULATOR, "VCC_DDR_IO", 4.397),
    ("get_VCC_SOC_IO", ElementType.REGULATOR, "VCC_SOC_IO", 5.397),
    ("get_VCC_GBE_IO", ElementType.REGULATOR, "VCC_GBE_IO", 6.397),
    ("get_VCC_USB_IO", ElementType.REGULATOR, "VCC_USB_IO", 7.397),
    ("get_VCC_BOOT_AUX", ElementType.REGULATOR, "VCC_BOOT_AUX", 8.397),
    ("get_VCC_SOC_AUX", ElementType.REGULATOR, "VCC_SOC_AUX", 9.397),
    ("get_VCC_GBE_AUX", ElementType.REGULATOR, "VCC_GBE_AUX", 10.397),
    ("get_VCC_USB_AUX", ElementType.REGULATOR, "VCC_USB_AUX", 11.397),
    ("get_VCC_PUF", ElementType.REGULATOR, "VCC_PUF", 12.397),
    ("get_VCC_RC_OSC", ElementType.REGULATOR, "VCC_RC_OSC", 13.397),
])
def test_power_coeff_method(mock_device, method_name, element_type, coef_name, coef_value):
    with patch('submodule.rs_device_resources.RsPowerConfig') as MockRsPowerConfig:
        MockRsPowerConfig.return_value.get_coeff.return_value = coef_value
        device_resources = RsDeviceResources(mock_device)
        method = getattr(device_resources, method_name)
        result = method()
        MockRsPowerConfig.return_value.get_coeff.assert_called_with(element_type, coef_name)
        assert coef_value == result
