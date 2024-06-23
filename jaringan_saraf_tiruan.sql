-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 23, 2024 at 09:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jaringan_saraf_tiruan`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_model`
--

CREATE TABLE `tbl_m_model` (
  `id_tmm` int(11) NOT NULL,
  `nama_model_tmm` text NOT NULL,
  `scaler_tmm` text NOT NULL,
  `encoder_tmm` text NOT NULL,
  `waktu_tmm` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_model`
--

INSERT INTO `tbl_m_model` (`id_tmm`, `nama_model_tmm`, `scaler_tmm`, `encoder_tmm`, `waktu_tmm`) VALUES
(1, 'model_20240622052842.h5', '', '', '2024-06-21 22:28:42'),
(2, 'model_20240622053652.h5', '', '', '2024-06-21 22:36:52'),
(3, 'model_20240622054124.h5', '', '', '2024-06-21 22:41:24'),
(4, 'model_20240622054213.h5', '', '', '2024-06-21 22:42:13'),
(5, 'model_20240622054449.h5', '', '', '2024-06-21 22:44:49'),
(6, 'model_20240622054503.h5', '', '', '2024-06-21 22:45:03'),
(7, 'model_20240622054653.h5', '', '', '2024-06-21 22:46:53'),
(8, 'model_20240622054721.h5', '', '', '2024-06-21 22:47:21'),
(9, 'model_20240622055455.h5', '', '', '2024-06-21 22:54:55'),
(10, 'model_20240623142809.h5', '', '', '2024-06-23 07:28:09'),
(11, 'model_20240623143705.h5', 'scaler_20240623143705.pkl', 'encoder_20240623143705.pkl', '2024-06-23 07:37:05'),
(12, 'model_20240623143726.h5', 'scaler_20240623143726.pkl', 'encoder_20240623143726.pkl', '2024-06-23 07:37:26');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_output`
--

CREATE TABLE `tbl_m_output` (
  `id_tmo` int(10) NOT NULL,
  `output_tmo` varchar(50) NOT NULL,
  `keterangan_tmo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_output`
--

INSERT INTO `tbl_m_output` (`id_tmo`, `output_tmo`, `keterangan_tmo`) VALUES
(1, 'Otoriter', 'Pola Asuh Otoriter'),
(4, 'Permisif', 'Permisif'),
(5, 'Demokratis', 'Demokratis'),
(6, 'Tidak Terlibat', 'Tidak Terlibat');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_users`
--

CREATE TABLE `tbl_m_users` (
  `id_tmu` int(10) NOT NULL,
  `username_tmu` varchar(50) NOT NULL,
  `password_tmu` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_users`
--

INSERT INTO `tbl_m_users` (`id_tmu`, `username_tmu`, `password_tmu`) VALUES
(1, 't', 'e358efa489f58062f10dd7316b65649e');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_variabel`
--

CREATE TABLE `tbl_m_variabel` (
  `id_tmv` int(10) NOT NULL,
  `variabel_tmv` varchar(50) NOT NULL,
  `kategori_tmv` enum('rendah','sedang','tinggi','') NOT NULL,
  `pertanyaan_tmv` text NOT NULL,
  `id_tmo` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_variabel`
--

INSERT INTO `tbl_m_variabel` (`id_tmv`, `variabel_tmv`, `kategori_tmv`, `pertanyaan_tmv`, `id_tmo`) VALUES
(4, 'Kebahagian', 'rendah', 'Kebahagian', 1),
(5, 'Prestasi Akademik', 'sedang', 'Prestasi Akademik', 1),
(6, 'Kebahagian', 'rendah', 'Kebahagian', 4),
(7, 'Prestasi Akademik', 'sedang', 'Prestasi Akademik', 4),
(8, 'Kebahagian', 'sedang', 'Kebahagian', 6),
(9, 'Prestasi Akademik', 'rendah', 'Prestasi Akademik', 6),
(10, 'Kebahagian', 'tinggi', 'Kebahagian', 5),
(11, 'Prestasi Akademik', 'tinggi', 'Prestasi Akademik', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_m_model`
--
ALTER TABLE `tbl_m_model`
  ADD PRIMARY KEY (`id_tmm`);

--
-- Indexes for table `tbl_m_output`
--
ALTER TABLE `tbl_m_output`
  ADD PRIMARY KEY (`id_tmo`);

--
-- Indexes for table `tbl_m_users`
--
ALTER TABLE `tbl_m_users`
  ADD PRIMARY KEY (`id_tmu`);

--
-- Indexes for table `tbl_m_variabel`
--
ALTER TABLE `tbl_m_variabel`
  ADD PRIMARY KEY (`id_tmv`),
  ADD KEY `id_tmo` (`id_tmo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_m_model`
--
ALTER TABLE `tbl_m_model`
  MODIFY `id_tmm` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `tbl_m_output`
--
ALTER TABLE `tbl_m_output`
  MODIFY `id_tmo` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tbl_m_users`
--
ALTER TABLE `tbl_m_users`
  MODIFY `id_tmu` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_m_variabel`
--
ALTER TABLE `tbl_m_variabel`
  MODIFY `id_tmv` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_m_variabel`
--
ALTER TABLE `tbl_m_variabel`
  ADD CONSTRAINT `tbl_m_variabel_ibfk_1` FOREIGN KEY (`id_tmo`) REFERENCES `tbl_m_output` (`id_tmo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
